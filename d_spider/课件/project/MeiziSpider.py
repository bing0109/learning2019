import requests
from bs4 import BeautifulSoup
import os
import time
from fake_useragent import UserAgent

def get_response(url):
    '''
    获得响应
    :param url: 请求url
    :return:
    '''
    html=requests.get(url).text
    # time.sleep(1)
    return html

def get_page_url(url):
    '''
    获得主题的url和对应的页码数
    :param url: 首页的url
    :return:
    '''
    html = get_response(url)#进行请求，获得响应
    soup = BeautifulSoup(html,'html.parser')#解析成BeautifulSoup对象
    results=soup.select('.pic li > a')#定位到包含主题url的节点
    for result in results:
        page_url=result['href']#获取主题url
        html_page=get_response(page_url)#进行请求，获得响应
        soup_page = BeautifulSoup(html_page,'html.parser')
        page=soup_page.select('#page a')[-2].string#提取页码信息
        yield page_url,page

def get_img(page_url,pn):
    '''
    获得图片，进行保存
    :param page_url: 主题url
    :param pn: 页数
    :return:
    '''
    base_url = page_url + '/' + str(pn)#构建翻页后的url
    html = get_response(base_url)#进行请求
    soup = BeautifulSoup(html,'html.parser')
    img_url=soup.select('#content a img')[0].attrs['data-img']#提取图片url

    headers={
        'Referer':page_url+'/'+str(pn-1),
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    response=requests.get(img_url,headers=headers,allow_redirects=False)#对图片url进行请求，获得响应
    print(base_url,response.status_code)
    if response.status_code == 200:#判断状态码是否为200
        img_name=img_url.split('/')[-2]+'-'+img_url.split('/')[-1]#图片的文件名
        #保存图片
        with open(img_name,'wb') as f:
            f.write(response.content)

#主体函数
def main():
    '''
    主体函数:先获取对应主题url，然后获取该主题下的页码信息，
             之后基于页码信息和主题url获取对应的图片url，
             最后获取图片二进制流，并进行保存
    :return:
    '''
    #创建保存图片的文件夹
    if not os.path.exists('xxoo'):
        os.mkdir('xxoo')
    #切换路径
    os.chdir('xxoo')
    url='http://www.mmjpg.com/tag/mengmei'
    pages=get_page_url(url)#获取主题的url，返回的是生成器
    # print(pages)
    for page_url,page in pages:#每个主题下的url以及页码数
        for pn in range(1,int(page)+1):#翻页
            get_img(page_url,pn)#获取图片并进行保存

if __name__=='__main__':
    main()