import requests
from bs4 import BeautifulSoup
import os
import time
import pymongo
import random

mongo_client = pymongo.MongoClient('localhost', 27017)
db = mongo_client.pachong
collection = db.meizitu

base_data_dir = '/home/zelin/data/meizitu/img/'


def save_mongo(detail):
    # collection.insert_one(detail)
    pass


def save_img(img_url, pre_url):
    headers = {
        'referer': pre_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    res = requests.get(img_url, headers=headers, allow_redirects=False)
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
    else:
        print(res.status_code)

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

    headers = {
        'referer': referer_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    print(url,referer_url, '--url--refer--')
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

        detail = {
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

        for type_pg in range(1, int(detail['nums'])+1):
            if type_pg == 1:
                img_path = save_img(detail['url_img'], url)
                detail['img_path'] = img_path
                print(detail, '---nums---')
                save_mongo(detail)
            else:
                # 获取第二页之后的数据,要先请求第二页,获得图片url,再请求url获取图片content
                next_url = type_url + '/' + str(type_pg)

                next_url_prev = type_url + '/' + str(type_pg-1)
                pre_url = get_img_url_next_all(next_url, type_pg, url, next_url_prev)
                detail['url_img'] = pre_url
                img_path = save_img(detail['url_img'], next_url)
                detail['img_path'] = img_path
                print(detail, '---nums---')
                save_mongo(detail)

            time.sleep(random.randint(1, 5))


def main():

    for pg in range(1, 2):
        if pg == 1:
            url = 'http://www.mmjpg.com/'

        else:
            url = 'http://www.mmjpg.com/home/' + str(pg)

        get_img_nums(url, pg)


if __name__ == '__main__':
    main()
