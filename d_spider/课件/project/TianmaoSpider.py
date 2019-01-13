from urllib import request
import json
import pymongo
from fake_useragent import UserAgent
import time

MONGO_URL='localhost'
MONGO_DB='Tianmao'
MONGO_COLLECTION = 'bra'

client = pymongo.MongoClient(host=MONGO_URL,port=27017)#建立客户端
db = client[MONGO_DB]#指明针对的是哪一个DB

def save_info(info):
    '''
    保存数据，通过updata函数进行数据更新，如果已经存在数据库，则更新，否则插入数据
    :param info: 需要保存的数据
    :return:
    '''
    if db[MONGO_COLLECTION].update({'id':info['id']},{'$set':info},True):
        print('保存成功',info)
    else:
        print('保存失败',info)

def get_response(url):
    '''
    进行请求：请求天猫，需要获取进行登录，所以在请求头里面添加cookie
    获得响应：因为响应体信息类似json字符串,所以可以进行调用json库进行处理，
    :param url: 请求的url
    :return: 返回转化成字典格式的响应体信息
    '''
    ua = UserAgent()
    headers={
        'referer': 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.4.3b762beaQGdqZY&id=564593555827&skuId=3959386545201&areaId=440300&user_id=2917184910&cat_id=2&is_b=1&rn=a833790271a008a9ba2a9bbfc2204dc3',
        'cookie': 'x=__ll%3D-1%26_ato%3D0; t=2a7c9eec7ad84a1dfd0aabd34ae30374; lid=%E4%B8%80%E6%98%9F%E4%BA%AE%E5%85%890513; _tb_token_=5a847337761d6; cookie2=1ade9883f3f5e4e52785293b48faabb3; hng=""; cna=rZFmFJedX2oCAXQYQhNNBuVz; enc=7vHbIFIbb3xcosNdiBKpiDvjEOoN0JoEVoCgn0rSANcp%2BNHI%2FECmY4UGZ2mTE4FuxjrA2vTIoGGEHZYoWlbEgQ%3D%3D; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x5sec=7b22726174656d616e616765723b32223a223436333030636132313633333630303235303565363538313237303237336535434f3672304f4546454f7a743459766a794d66764e686f4d4d5441304e6a49774d5463304d6a7378227d; uc1=cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie21=VT5L2FSpczFp&cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=false&pas=0&cookie14=UoTYMDKceQiRig%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByRIpaOiCsBICBJk%3D&id2=VAmskEGL54Vx&nk2=sa32It89oG0%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; tracknick=%5Cu53F6%5Cu98CE%5Cu8FD021; _l_g_=Ug%3D%3D; ck1=""; unb=786283128; lgc=%5Cu53F6%5Cu98CE%5Cu8FD021; cookie1=BqOyRGVQdnFDYe2vnuApTsHo5TqOh%2FqFDnblnAbnG1Q%3D; login=true; cookie17=VAmskEGL54Vx; _nk_=%5Cu53F6%5Cu98CE%5Cu8FD021; uss=""; csg=db024e4d; skt=c865b73817128600; whl=-1%260%260%260; l=aBWHLKOOybeUKWEBtMa4gNy4y707mhfPe6UL1MayzTEhNzOrCI5HcnnoWMsk8_0WTw1NOouHIWs..; isg=BEZGPUP2ZmWa1TVRZNxQin6elzwID40WqsjsBjBvEmlGM-dNmDZjcTSFDy9am4J5',
        'user-agent':ua.random
    }
    request1 = request.Request(url=url,headers=headers,method='GET')
    repsonse=request.urlopen(request1)#请求
    time.sleep(1)
    html=repsonse.read().decode('utf8').replace('jsonp1601(','').replace(')','')#处理
    result=json.loads(html)#转化为字典
    return result

#获取页码信息
def get_page(url):
    '''
    获得页码信息
    :param url: 请求的url
    :return: 页码信息
    '''
    result = get_response(url)
    page=result['rateDetail']['paginator']['lastPage']
    return page

def get_info(url):
    '''
    获取每一页的评论信息
    :param url:
    :return:
    '''
    result = get_response(url)
    infos=result['rateDetail']['rateList']
    for info in infos:
        info_bra={
            'color':info['auctionSku'].split(';')[0][5:],#颜色
            'size': info['auctionSku'].split(';')[-1][3:],#尺寸
            'id':info['id'],#评论id
            'rateContent':info['rateContent']#评论信息
        }
        save_info(info_bra)#保存到数据库


#主体函数
def main():
    url='https://rate.tmall.com/list_detail_rate.htm?itemId=564593555827&spuId=927986671&sellerId=2917184910&order=3&currentPage=1&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvWpvRvphvUvCkvvvvvjiPR2dy1jDbn2cvsjthPmPZ1jE2PFqwgjiPRLLwgj3ERphvCvvvphm5vpvhvvCCBvhCvvOvChCvvvmtvpvIvvCvpvvvvvvvvhZLvvvvTpvvBBWvvUhvvvCHhQvvv7QvvhZLvvvCf8yCvv9vvhhid8mICIyCvvOCvhE20nQEvpCW9PjQGC0v%2BiT7ej%2BEIWQ7VB4A4xbX3LypRigrvGVYRCoZHkGoz4ZzWdJqV0Yl%2BboJhLIImKADDXgB%2B0ERi4AJhfoAOyTDdEgBE2OiovGCvvpvvPMMRphvCvvvphmjvpvhvUCvpUhCvv147sqzya147DiagaGtvpvhvvCvp86Cvvyv9BwwGQvvCyKCvpvZ7DlKJjsw7Di4a%2Bq5PjE4Ylulz1h%3D&needFold=0&_ksTS=1546912296575_1600&callback=jsonp1601'
    page=get_page(url)#获取页码信息
    for pn in range(1,page+1):#翻页
        base_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=564593555827&spuId=927986671&sellerId=2917184910&order=3&currentPage='+str(pn)+'&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvWpvRvphvUvCkvvvvvjiPR2dy1jDbn2cvsjthPmPZ1jE2PFqwgjiPRLLwgj3ERphvCvvvphm5vpvhvvCCBvhCvvOvChCvvvmtvpvIvvCvpvvvvvvvvhZLvvvvTpvvBBWvvUhvvvCHhQvvv7QvvhZLvvvCf8yCvv9vvhhid8mICIyCvvOCvhE20nQEvpCW9PjQGC0v%2BiT7ej%2BEIWQ7VB4A4xbX3LypRigrvGVYRCoZHkGoz4ZzWdJqV0Yl%2BboJhLIImKADDXgB%2B0ERi4AJhfoAOyTDdEgBE2OiovGCvvpvvPMMRphvCvvvphmjvpvhvUCvpUhCvv147sqzya147DiagaGtvpvhvvCvp86Cvvyv9BwwGQvvCyKCvpvZ7DlKJjsw7Di4a%2Bq5PjE4Ylulz1h%3D&needFold=0&_ksTS=1546912296575_1600&callback=jsonp1601'
        get_info(base_url)#获取每一页的评论数据

if __name__=='__main__':
    main()