# coding=utf8
import sys
import os
import requests
from bs4 import BeautifulSoup
import time
import pymongo
import random
import logging
import copy
from fake_useragent import UserAgent

# 日志配置
logging.basicConfig(
    level=logging.INFO,    # 打印日志的级别
    filename='/home/zelin/data/meizitu/meizitu.log',  # 指定写日志的文件
    filemode='a',                                       # 模式，a 追加， w 覆盖写入
    # format='%(asctime)s - %(levelname)s - %(pathname)s[line:%(lineno)d]: %(message)s',
    # 日志格式,%(pathname)s[line:%(lineno)d]是发生写日志记录的代码文件和行号
    format='%(asctime)s - %(levelname)s - line:%(lineno)d: %(message)s',
)


mongo_client = pymongo.MongoClient('localhost', 27017)
db = mongo_client.pachong
collection = db.meizitu

base_data_dir = '/home/zelin/data/meizitu/img/'

proxy_pool = [
    'http://119.101.114.236:9999',
    'http://27.29.46.70:9999',
    'http://114.106.150.44:9999',
    'http://123.163.115.51:9999',
]

def save_mongo(detail, img_path):
    if collection.delete_many({'url_img': str(detail['url_img'])}).deleted_count > 0:
        logging.warning('delete old in mongo;' + str(detail))

    try:
        collection.insert_one(detail)
        logging.info('save mongo success;' + str(img_path))
    except Exception as e:
        logging.error('save mongo fail;' + str(img_path) + '\n' + str(e))

    # collection.insert_one(detail)


def save_img(img_url, pre_url):
    headers = {
        'referer': pre_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    proxies = proxy_pool[random.randint[0,len(proxy_pool)+1]]

    res = requests.get(img_url, headers=headers, proxies=proxies, verify=False ,allow_redirects=False)
    temp_name = img_url.split('/')
    # 根据url形成图片路径和名称
    img_path = base_data_dir + str(temp_name[3]) + '/' + str(temp_name[4])
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    img_name = str(temp_name[5])

    if res.status_code == 200:
        img_path = base_data_dir + str(temp_name[3]) + '/' + str(temp_name[4])
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        img_name = str(temp_name[5])

        with open(img_path + '/' + img_name, 'wb') as f:
            f.write(res.content)
        logging.info('save img success' + str(img_path + '/' + img_name))

    else:
        print(res.status_code)
        logging.error('save img fail' + str(img_url))

    return str(img_path + '/' + img_name)


def get_photo_list(url, pg):
    """
    获取每一页中每个div中图片指向的链接
    :param url:
    :param pg:
    :return:
    """
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    photo_list = soup.select('body > div.main > div.pic > ul > li')
    print(len(photo_list))
    for photo in photo_list:
        type_url = photo.select('span.title > a')[0]['href']
        yield(type_url)


def get_img_url_next_all(url, page_num, pre_url_2pg, pre_url_temp_after2pg):
    """
    获取每种主题第2页之后的图片的链接
    :param url:
    :param page_num:
    :return:
    """

    if page_num > 2:
        referer_url = pre_url_2pg
    else:
        referer_url = pre_url_temp_after2pg

    ua = UserAgent()

    headers = {
        'referer': referer_url,
        'user-agent': ua.random,
    }
    print(headers,'-----headers-----')
    # print(url, referer_url, '--url--refer--')
    res = requests.get(url, headers=headers, allow_redirects=False).text
    soup = BeautifulSoup(res, 'lxml')
    url_img = soup.select('#content > a > img')[0]['src']  # 每个主题的第一页的图片的链接
    return url_img


def get_img_nums(url, pg):
    """
    获取每种主题图片的第一张图片的链接和图片数量
    :param url:
    :param pg:
    :return:
    """
    type_urls = get_photo_list(url, pg)
    for type_url in type_urls:
        res = requests.get(type_url).content.decode('utf-8')
        soup = BeautifulSoup(res, 'lxml')
        url_img = soup.select('#content > a > img')[0]['src']     # 每个主题的第一页的图片的链接
        nums = soup.select('#opic')[0].previous_sibling.get_text()      # 每个主题的第一页中获取 该主题图片数量
        title = soup.select('body > div.main > div.article > h2')[0].get_text()
        release_time = soup.select('body > div.main > div.article > div.info > i:nth-of-type(1)')[0].get_text()[4:]
        source = soup.select('body > div.main > div.article > div.info > i:nth-of-type(2)')[0].get_text()[3:]
        looks = soup.select('body > div.main > div.article > div.info > i:nth-of-type(4)')[0].get_text()[3:-1]
        favs = soup.select('body > div.main > div.article > div.info > i:nth-of-type(5)')[0].get_text()[3:-1]

        detail_tem = {
            'type_url': type_url,
            'url_img': url_img,
            'img_path': '',
            'nums': nums,
            'title': title,
            'release_time': release_time,
            'source': source,
            'looks': looks,
            'favs': favs,
        }

        for type_pg in range(1, int(nums)+1):
            detail = copy.deepcopy(detail_tem)  # 要重新定义dict,不然存mongo的时候会认为是同一个dict给存成同一个id了,导致主键冲突存不进去
            if type_pg == 1:
                try:
                    img_path = save_img(detail['url_img'], url)
                    detail['img_path'] = img_path
                    # print(detail, '---nums---')
                    save_mongo(detail, img_path)
                except Exception as e1:
                    logging.error('save info1 fail' + str(detail) + '\n' + str(e1))
            else:
                try:
                    # 获取第二页之后的数据,要先请求第二页,获得图片url,再请求url获取图片content
                    next_url = type_url + '/' + str(type_pg)
                    next_url_prev = type_url + '/' + str(type_pg-1)
                    pre_url = get_img_url_next_all(next_url, type_pg, url, next_url_prev)
                    detail['url_img'] = pre_url
                    img_path = save_img(detail['url_img'], next_url)
                    detail['img_path'] = img_path
                    # print(detail, '---nums2---')
                    save_mongo(detail, img_path)
                except Exception as e2:
                    logging.error('save info2 fail' + str(detail) + '\n' + str(e2))

            time.sleep(random.randint(1, 4))


def main():

    for pg in range(1, 100):
        if pg == 1:
            url = 'http://www.mmjpg.com/'

        else:
            url = 'http://www.mmjpg.com/home/' + str(pg)

        get_img_nums(url, pg)


if __name__ == '__main__':
    main()
