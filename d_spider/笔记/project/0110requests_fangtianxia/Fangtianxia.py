import requests
from bs4 import BeautifulSoup
import time
import random
import pymongo

Mongo_url = 'localhost'
Mongo_db = 'House'
Mongo_collection = 'Fangtianxia'

my_mongo_client = pymongo.MongoClient(Mongo_url, 27017)
my_mongo_db = my_mongo_client.Mongo_db
ftx_collection = my_mongo_db[Mongo_collection]      # 房天下的数据存到这个数据库集合中


def save_mongodb(data_info):
    """
    保存数据库到数据库
    :param data_info:
    :return:
    """
    url_check = ftx_collection.find({'data_link': str(data_info['data_link'])})

    # 去重，删除数据库中已经存在的记录，在后面的if中重新插入
    if len(list(url_check)) > 0:
        ftx_collection.delete_many({'data_link': str(data_info['data_link'])})
        print('delete old', data_info['data_link'])

    if ftx_collection.insert_one(data_info):
        print('save success', data_info)
    else:
        print('save fail', data_info)


def get_response(url):
    """
    根据每一页的url进行请求，并解析出 房价信息的列表
    :param url:
    :return:
    """
    # res = requests.get(url).content.decode('GB18030')
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    # 不同的编译环境，有些不生效,用lxml在本地3.5的编译环境下是生效的，在anaconda下会取不到数据
    # soup = BeautifulSoup(res, 'lxml')
    data_div_list = soup.select('div.houseList .list')
    print(len(data_div_list), '---len every page---')
    return data_div_list


def get_info(info):
    """
    根据传进来的每一条房价信息记录，提取出相关字段，并返回字典格式
    :param info:
    :return:
    """
    data_link = 'https:' + info.select('dl dt a')[0]['href']
    data_name = info.select('dl dd p:nth-of-type(1) a')[0].get_text()
    data_house_type = info.select('dl dd p:nth-of-type(1) .plotFangType')[0].get_text()
    data_score_no2 = len(info.select('dl dd p:nth-of-type(1) .dj .no2'))
    data_score_half = len(info.select('dl dd p:nth-of-type(1) .dj .half'))
    data_score = str(5 - data_score_no2 - data_score_half*0.5)
    data_address = info.select('dl > dd > p:nth-of-type(2)')[0].get_text().strip()
    data_district = data_address.split(' ')[0].split('-')[0]
    data_street = data_address.split(' ')[0].split('-')[1]
    data_addr_detail = data_address.split(' ')[1].replace(',', '-')
    data_sold_num = info.select('dl dd ul li')[0].select('a')[0].get_text().strip()
    data_rent_num = info.select('dl dd ul li')[1].select('a')[0].get_text().strip()
    data_build_year = info.select('dl dd ul li')[2].get_text().strip()[:4]
    data_house_price = info.select('.listRiconwrap .priceAverage span:nth-of-type(1)')[0].get_text().strip() if len(info.select('.listRiconwrap .priceAverage span:nth-of-type(1)')) > 0 else 'no data'
    data_house_ratio = info.select('.listRiconwrap .ratio span')[0].get_text().strip().replace('↑', '+').replace('↓', '-') if len(info.select('.listRiconwrap .ratio span')) > 0 else 'no data'

    detail = {
        'data_link': data_link,
        'data_name': data_name,
        'data_house_type': data_house_type,
        'data_score': data_score,
        'data_district': data_district,
        'data_street': data_street,
        'data_addr_detail': data_addr_detail,
        'data_rent_num': data_rent_num,
        'data_sold_num': data_sold_num,
        'data_build_year': data_build_year,
        'data_house_price': data_house_price,
        'data_house_ratio': data_house_ratio,
    }
    # print(detail)
    return detail


def main():
    total_page = 100

    # 保存在文件中
    # with open('ftx.csv', 'w') as f:
    #     f.write('data_link, data_name, data_house_type, data_score, data_district, data_street, data_addr_detail, data_rent_num, data_sold_num, data_build_year, data_house_price, data_house_ratio \n')
    #     for i in range(1, total_page+1):
    #         print(i)
    #         time.sleep(random.randint(1, 5))
    #         url = 'https://sz.esf.fang.com/housing/__0_0_0_0_' + str(i) + '_0_0_0/'
    #         res_info = get_response(url)
    #         for info in res_info:
    #             data_info = get_info(info)
    #             string = data_info['data_link'] + ',' + data_info['data_name'] + ',' + data_info['data_house_type'] + ',' + data_info['data_score'] + ',' + data_info['data_district'] + ',' + data_info['data_street'] + ',' + data_info['data_addr_detail'] + ',' + data_info['data_rent_num'] + ',' + data_info['data_sold_num'] + ',' + data_info['data_build_year'] + ',' + data_info['data_house_price'] + ',' + data_info['data_house_ratio'] + ',' + '\n'
    #             f.write(string)

    # 保存在数据库中
    # # 翻页
    for i in range(1, total_page+1):
        print(i)
        time.sleep(random.randint(1, 5))
        url = 'https://sz.esf.fang.com/housing/__0_0_0_0_' + str(i) + '_0_0_0/'
        res_info = get_response(url)
        # print(len(res_info), '----')
        for info in res_info:
            data_info = get_info(info)
            save_mongodb(data_info)
            # print('---23----')


if __name__ == '__main__':
    main()
