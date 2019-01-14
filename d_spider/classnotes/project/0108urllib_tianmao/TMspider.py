from urllib import request
import json
# import pymongo


def get_response(url):
    header = {
        'referer': 'https://list.tmall.com/search_product.htm?q=%B9%AB%C5%A3%B2%E5%D7%F9&type=p&vmarket=&spm=a211oj.12451259.a2227oh.d100&xl=%B9%AB%C5%A3_1&from=..pc_1_suggest',
        '': ''
    }
    response = request.urlopen(url)
    print(type(response))
    print(response.url)
    # 用utf-8解码报错，可以尝试用其他的中文编码
    # res_data = response.read().decode('utf-8').replace('jsonp781(', '').replace(')', '')
    res_data = response.read().decode('utf-8').replace('jsonp781(', '').replace(')', '')
    temp_data = json.load(res_data)
    # 上两步，把返回的jsonp转换成字典
    data_list = temp_data['rateDetail']['rateList']
    result = {}
    for data in data_list:
        result['id'] = data['id']
        result['comment'] = data['rateContent']
        result['color'] = data['auctionSku']
    print(result)
    return result


def main():
    # with open('tiamao.csv', 'wb') as f:
    for i in range(1, 2):
        url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=528689955359&spuId=473298610&sellerId=1772233696&order=3&currentPage=' + str(i) + '&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvc9vLvZ6vUvCkvvvvvjiPR2Svsj1RRsdvtjljPmPw6jlhnLzyAj3nP2LhzjlRRphvChCvvvmrvpvEphH82HpvBVV7dphvmZCmr3vvvh2aDu6CvvDvpuWZvpCvLevtvpvhphvvvUhCvCgJP8XJXYMwzn1aDxis9TkUmOV%2FQ%2FUqAwkCoWfEwQR5vpvhphvhH2yCvvBvpvvvvphvCyCCvvvvvvyCvh12yHUvItgDN5Od%2B87J%2B3%2BuwosG0EyfaZY0pK2hHF%2BSBkphQRA1%2B2n7OHfIAfUTnZwK2ixreutYVC%2BKa4QB%2BAxGOyTDYE9waZx%2BVd0DkphvCyEmmvkfe8yCvv3vpvo3Vw6zYqyCvm3vpvC9vvCvaZCvHUpvvhb2phvZ7pvvp6nvpCohvvCmuyCvHUpvvh8u2QhvCvvvMM%2Fjvpvhphhvv86CvvDvpPpZdQCvfivjvpvjzn147SMQ%2F2yCvvBvpvvv9phvHnsGqH6azYswcUVg7%2FJozEcwmliI&needFold=0&_ksTS=1547037550523_780&callback=jsonp781'
        get_response(url)


if __name__ == '__main__':
    main()
