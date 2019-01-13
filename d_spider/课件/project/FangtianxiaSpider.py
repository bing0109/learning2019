import requests
from bs4 import BeautifulSoup
import pymongo
import time

MONGO_URL = 'localhost'
MONGO_DB = 'House'
MONGO_NAME = 'Fangtianxia'

client = pymongo.MongoClient(MONGO_URL)#连接数据库，创建客户端
db = client[MONGO_DB]#说明针对哪一个数据库

def save_mongo(info):
    '''
    保存数据到数据库
    :param info: 需要保存的数据，字典形式
    :return:
    '''
    if db[MONGO_NAME].insert_one(info):
        print('保存成功',info)
    else:
        print('保存失败',info)

def get_response(url):
    '''
    进行请求，并获得响应
    需要注意的是：获取响应体时，由于涉及中文乱码的问题，需要考虑解码
    :param url: 请求url
    :return: 返回响应体
    '''
    html=requests.get(url).content.decode('gb18030')
    time.sleep(2)
    return html

def get_info(html):
    # print(html)
    soup = BeautifulSoup(html,'html.parser')
    results=soup.select('.houseList .list')#定位到包含所有小区信息的节点列表
    for result in results:
        #分数处理
        half = len(result.select('dd .dj .half'))
        no2 = len(result.select('dd .dj .no2'))
        #地址处理
        address1=result.select('dd > p:nth-of-type(2)')[0].get_text()
        # print(address1.get_text().strip())
        info={
            'url':result.select('dd > p > a')[0]['href'],#小区链接
            'name': result.select('dd > p > a')[0].string,#小区名
            'score':5-0.5*half-no2,#小区评分
            'area':address1.split('-')[0].strip(),#区域
            'business':address1.split('-')[1].strip().split(' ')[0].strip(),#商区
            'address':address1.split('-')[1].strip().split(' ')[1].strip(),#地址
            'year':result.select('dd ul.sellOrRenthy li')[-1].get_text()[:4],#建成时间
            'price':result.select('.priceAverage span')[0].get_text().strip() if len(result.select('.priceAverage span')) > 0 else None#价格
        }
        save_mongo(info)#保存数据

#主体函数
def main():
    page=100
    for i in range(1,page+1):#翻页
        print(i)
        url='https://sz.esf.fang.com/housing/__1_0_0_0_'+str(i)+'_0_0_0/'
        html=get_response(url)#请求，并获得响应
        get_info(html)#提取信息，并进行保存
    client.close()#关闭数据库

if __name__=='__main__':
    main()