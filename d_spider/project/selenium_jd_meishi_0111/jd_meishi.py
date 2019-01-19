# coding=utf8
import sys
import os


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from bs4 import BeautifulSoup
import time
import pymongo
import requests
import random
import logging



# 日志配置
logging.basicConfig(
    level=logging.INFO,    # 打印日志的级别
    filename='/home/zelin/data/jdmeishi/jdmeishi.log',  # 指定写日志的文件
    filemode='a',                                       # 模式，a 追加， w 覆盖写入
    # format='%(asctime)s - %(levelname)s - %(pathname)s[line:%(lineno)d]: %(message)s',
    # 日志格式,%(pathname)s[line:%(lineno)d]是发生写日志记录的代码文件和行号
    format='%(asctime)s - %(levelname)s - line:%(lineno)d: %(message)s',
)


# mongodb连接
client = pymongo.MongoClient('localhost', 27017)
db = client.pachong
collection = db.jd_meishi


def save_mongo(detail, pg, good_list):
    # url_check = collection.find({'img_url': str(detail['img_url'])})
    # # 去重，删除数据库中已经存在的记录，在后面的if中重新插入
    # if len(list(url_check)) > 0:
    #     collection.delete_many({'img_url': str(detail['img_url'])})
    #     print('delete old in mongo', detail['img_url'])

    if collection.delete_many({'img_url': str(detail['img_url'])}).deleted_count > 0:
        logging.warning('delete old in mongo;' + str(detail))

    try:
        collection.insert_one(detail)
        logging.info('save success;' + str(pg) + '-' + str(good_list))
    except Exception as e:
        logging.error('save fail;' + str(pg) + '-' + str(good_list) + '\n' + str(e))


def save_img(url, path):
    '''
    这个模块要重新请求图片，耗时较大
    :param url:
    :param path:
    :return:
    '''
    try:
        img_res = requests.get(url).content
        with open(path, 'wb') as f:
            f.write(img_res)

        logging.info('save img success;' + str(path))

    except Exception as e:
        logging.error('save img error;' + str(path) + str(url) + '\n' + str(e))


def get_good_list(html, pg):
    soup = BeautifulSoup(html, 'html.parser')
    goods_list = soup.select('#J_goodsList > ul > li')
    print(len(goods_list), pg, '----num per page---')
    return goods_list


def get_good_info(good, pg, li_index):
    try:
        img_url = 'https:' + good.select('div > div.p-img > a > img')[0].attrs['src']
    except Exception:
        logging.warning('get img url through src failed;' + str(pg) + '-' + str(li_index))
        img_url = ''

    if img_url == '':
        try:
            img_url = 'https:' + good.select('div > div.p-img > a > img')[0].attrs['data-lazy-img']
        except Exception:
            img_url = ''
            logging.warning('get img url through data-lazy-image failed;' + str(pg) + '-' + str(li_index))



    price = good.select('div > div.p-price > strong > i')[0].get_text()
    title = good.select('div > div.p-name.p-name-type-2 > a > em')[0].get_text().strip()
    comment_num = good.select('div > div.p-commit > strong > a')[0].string
    try:
        shop_name = good.select('div > div.p-shop > span > a')[0].get_text()
    except Exception:
        shop_name = ''

    items = good.select('div > div.p-icons')[0].get_text().strip().replace('\n', '/')

    info_detail = {
        'img_url': img_url,
        'price': price,
        'title': title,
        'comment_num': comment_num,
        'shop_name': shop_name,
        'items': items,
        'img_path': ''
    }

    # print(info_detail)
    return info_detail


def get_search(browser, wait):
    try:
        input_kw = wait.until(EC.presence_of_element_located((By.ID, 'key')))
        # search_btn = browser.find_element_by_css_selector('#search > div > div.form > button')
        search_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#search > div > div.form > button')))
        time.sleep(1)
        input_kw.send_keys('零食')
        time.sleep(1)
        search_btn.click()
        time.sleep(3)
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        last_li = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList > ul > li:nth-of-type(60)')))  # 等待每页最后一条记录显示出来，最后一页可能得另外处理一下
        total_page = browser.find_element_by_css_selector('#J_bottomPage > span.p-skip > em:nth-of-type(1) > b').text   # 总页数
        return total_page
    except StaleElementReferenceException as e1:
        logging.error('---e1---' + str(e1))
        return get_search(browser, wait)

    except TimeoutException as e2:
        logging.error('---e2---' + str(e2))
        return get_search(browser, wait)


def next_page(pg, browser, wait):
    if pg == 1:
        good_list = get_good_list(browser.page_source, pg)
        for good in good_list:
            good_index = good_list.index(good)
            good_detail = get_good_info(good, pg, good_index)
            img_path = '/home/zelin/data/jdmeishi/img/' + str(pg) + '_' + str(good_index) + '.jpg'
            save_img(good_detail['img_url'], img_path)    # 重新请求图片，耗时较大
            good_detail['img_path'] = img_path
            save_mongo(good_detail, pg, good_index)

    else:
        try:
            pg_input = browser.find_element_by_css_selector('#J_bottomPage > span.p-skip > input')
            pg_btn = browser.find_element_by_css_selector('#J_bottomPage > span.p-skip > a')
            pg_input.clear()
            pg_input.send_keys(pg)
            pg_btn.click()
            time.sleep(1)
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            last_li = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList > ul > li:nth-of-type(60)')))
            good_list = get_good_list(browser.page_source, pg)
            for good in good_list:
                good_index = good_list.index(good)
                good_detail = get_good_info(good, pg, good_index)
                img_path = '/home/zelin/data/jdmeishi/img/' + str(pg) + '_' + str(good_index) + '.jpg'
                save_img(good_detail['img_url'], img_path)    # 重新请求图片，耗时较大
                good_detail['img_path'] = img_path
                save_mongo(good_detail, pg, good_index)
        except StaleElementReferenceException as e3:
            logging.error('---e3---' + str(e3))
            return next_page(pg, browser, wait)
        except TimeoutException as e4:
            logging.error('---e4---' + str(e4))
            return next_page(pg, browser, wait)


def main():
    if not os.path.exists('/home/zelin/data/jdmeishi/img'):
        os.makedirs('/home/zelin/data/jdmeishi/img')

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(executable_path=r'/usr/bin/chromedriver', chrome_options=options)
    # browser = webdriver.Chrome()
    browser.get('https://www.jd.com/')
    wait = WebDriverWait(browser, 30)

    # input_kw = wait.until(EC.presence_of_element_located((By.ID, 'key')))
    # # search_btn = browser.find_element_by_css_selector('#search > div > div.form > button')
    # search_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#search > div > div.form > button')))
    # time.sleep(1)
    # input_kw.send_keys('零食')
    # time.sleep(1)
    # search_btn.click()
    # time.sleep(3)
    # browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    # last_li = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList > ul > li:nth-of-type(60)')))   #等待每页最后一条记录显示出来，最后一页可能得另外处理一下
    # total_page = browser.find_element_by_css_selector('#J_bottomPage > span.p-skip > em:nth-of-type(1) > b')    # 总页数

    total_page = get_search(browser, wait)
    print(total_page, '--totol page--')

    # total_page = 2
    for i in range(54, int(total_page)):
        next_page(i, browser, wait)
        time.sleep(random.randint(1, 5))

    # print(browser.page_source)
    browser.close()


if __name__ == '__main__':
    main()
