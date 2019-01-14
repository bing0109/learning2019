# coding=utf-8

import requests
import re
import os
import time
import random
import pymongo
"""
爬取猫眼的top100数据，通过正则表达式爬取网页
"""


def get_response(url):
    res = requests.get(url).text

    res_list = re.findall(r'.*?(<dd>.*?<i class="board-index.*?</dd>).*?', res, re.S)
    # print(len(res_list), res_list)
    return res_list


mongo_client = pymongo.MongoClient('localhost', 27017)
db = mongo_client.pachong
collection = db.maoyan


def save_date_to_mongo(detail):
    check = collection.find({'img_url': str(detail['img_url'])})

    if len(list(check)) > 0:
        collection.delete_many({'img_url': str(detail['img_url'])})
        print('delete old data', detail)

    if collection.insert_one(detail):
        print('save_date_to_mongo success', detail)
    else:
        print('save to mongo failed', detail)


def get_info(html, f):
    # 传入一个信息列表元素，从里面提取字段
    # 一次提取所有字段，有一个提取不到就是空的了，比较费脑
    re_match = re.compile(r'<dd>.*?<img.*?data-src="(.*?)"'
                          r'.*?class="name".*?href="(.*?)"'
                          r'.*?>(.*?)</a>'
                          r'.*?class="star">(.*?)</p>'
                          r'.*?class="releasetime">(.*?)</p>'
                          r'.*?class="score"><i.*?>(.*?)</i><i.*?>(.*?)</i></p>', re.S)
    info = re.findall(re_match, html)
    # print(info, '---info---')
    # print(len(info), '----len info----')
    img_url = info[0][0]
    movie_url = 'https://maoyan.com' + info[0][1]
    name = info[0][2].strip().replace(',', '-')
    actors = info[0][3].strip().replace(',', '/').replace(';', '/')
    show_time = info[0][4].replace(',', ' ')
    score = str(info[0][5]) + str(info[0][6])

    # 单独获取每一个字段也是ok的
    # img_url = re.search(r'<dd>.*?<img.*?data-src="(.*?)"', html, re.S).group(1)
    # movie_url = 'https://maoyan.com' + re.findall(r'.*?class="name"><a href="(.*?)"', html, re.S)[0]
    # name = re.findall(r'.*?class="name">.*?">(.*?)</a>', html, re.S)[0]
    # actors = re.findall(r'.*?class="star">(.*?)</p>', html, re.S)[0].strip()[3:]
    # show_time = re.findall(r'.*?class="releasetime">(.*?)</p>', html, re.S)[0][5:]
    # tem_score = re.findall(r'.*?class="score"><i.*?>(.*?)</i><i.*?>(.*?)</i></p>', html, re.S)
    # # print(tem_score)
    # score = str(tem_score[0][0].strip()) + str(tem_score[0][1].strip())

    info_dict = {
        'img_url': img_url,
        'movie_url': movie_url,
        'name': name,
        'actors': actors,
        'show_time': show_time,
        'score': score,
        'img_path': '',
    }
    # print(info_dict)
    img_res = requests.get(info_dict['img_url'])
    if img_res.status_code == 200:
        img_name = '/home/zelin/data/maoyan/img/' + info_dict['name'] + '.jpg'
        info_dict['img_path'] = img_name
        with open(img_name, 'wb') as img_f:
            img_f.write(img_res.content)
    else:
        img_name = 'none'
        info_dict['img_path'] = img_name

    w_string = img_url + ',' + img_name + ',' + movie_url + ',' + name + ',' + actors + ',' + show_time + ',' + score + '\n'
    f.write(w_string)

    save_date_to_mongo(info_dict)
    return info_dict


def main():
    if not os.path.exists('/home/zelin/data/maoyan'):
        os.makedirs('/home/zelin/data/maoyan')

    if not os.path.exists('/home/zelin/data/maoyan/img'):
        os.makedirs('/home/zelin/data/maoyan/img')

    f = open('/home/zelin/data/maoyan/maoyan.csv', 'w')
    f.write('img_url' + ',' + 'img_name' + ',' + 'movie_url' + ',' + 'name' + ',' + 'actors' + ',' + 'show_time' + ',' + 'score' + '\n')

    for i in range(0, 100, 10):
        print(i)
        time.sleep(random.randint(1, 3))
        url = 'https://maoyan.com/board/4?offset=' + str(i)
        html_list = get_response(url)
        # print(len(html_list), '----len html list---')
        for html in html_list:
            get_info(html, f)

    f.close()


if __name__ == '__main__':
    main()
