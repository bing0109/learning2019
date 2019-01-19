from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException,TimeoutException,NoSuchElementException
from bs4 import BeautifulSoup
import time
import pymongo

KEYWORD='美食'

client = pymongo.MongoClient('localhost')#建立数据库客户端
db = client['JD']#针对的数据库

browser = webdriver.Chrome()#声明浏览器
wait = WebDriverWait(browser,10)#声明显式等待时间

def save_mongo(info):
    '''
    保存数据
    :param info:信息，字典形式
    :return:
    '''
    if db[KEYWORD].insert_one(info):
        print('保存成功',info)
    else:
        print('保存失败',info)

def get_search():
    '''
    网址访问，并进行搜索，判断页面跳转是否已经完成，并提取页码信息
    :return: 页码信息
    '''
    try:
        browser.get('https://www.jd.com')#访问网页
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#key')))#定位搜索框
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#search > div > div.form > button')))#定位搜索按钮
        input.clear()
        input.send_keys(KEYWORD)#输入文本
        button.click()#点击按钮
        time.sleep(1)
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)
        # 判断是否翻页成功
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList > ul')))
        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.m div.m-box-s1 ')))
        page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > em:nth-child(1)>b'))).text
        return page
    except TimeoutException:
        return get_search()

def next_page(pn):
    '''
    翻页，并提取信息
    :param pn: 翻页的页码信息
    :return:
    '''
    if pn==1:#判断，如果是在第一页，直接进行信息提取，并保存
        html=browser.page_source
        get_info(html)#获取信息，并保存
    else:
        try:
            #页码输入框
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > input')))
            #确认按钮
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > a')))
            input.clear()#清空输入框
            input.send_keys(pn)#输入页码
            button.click()#点击按钮
            time.sleep(1)
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1)
            # 判断是否翻页成功
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList > ul')))
            wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(pn)))
            get_info(browser.page_source)#获取信息
        except StaleElementReferenceException:
            next_page(pn)
        except TimeoutException:
            next_page(pn)

def get_info(html):
    '''
    获取信息，并保存
    :param html: 当前页的html源码字符串
    :return:
    '''
    soup = BeautifulSoup(html,'html.parser')
    results=soup.select('#J_goodsList > ul > li.gl-item')#选择所有包含商品信息的节点
    for result in results:
        info={
            'url':result.select('.p-img > a')[0].attrs['href'],#商品详细信息url
            'price':result.select('.p-price i')[0].get_text(),#商品价格
            'name':result.select('.p-name > a > em')[0].get_text().strip(),#商品描述
            #商品评价数
            'commit':result.select('.p-commit > strong > a')[0].get_text().strip()[:-1],
            #店铺
            'shop':'京东自营' if len(result.select('.p-shop > span > a'))==0 else result.select('.p-shop > span > a')[0].get_text()
        }
        save_mongo(info)#保存数据

#主体函数
def main():
    page=get_search()#访问网页，并进行搜索
    for pn in range(1,int(page)+1):
        print(pn)
        next_page(pn)#翻页，并提取信息
    browser.close()#关闭浏览器

if __name__=='__main__':
    main()