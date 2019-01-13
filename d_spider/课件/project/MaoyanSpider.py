import requests
import re
import os

def get_response(url):
    '''
    获得响应
    :param url: 请求url
    :return: 返回响应体信息
    '''
    html=requests.get(url).text
    return html

def get_info(html,f):
    '''
    提取信息：通过正则表达式提取信息
    保存信息：将信息保存到csv文件，需要逐行保存
    :param html: 响应提信息，即html字符串
    :param f: 对应打开的文件
    :return:
    '''
    pattern=re.compile(r'<dd>.*?<img.*?data-src="(.*?)".*?class="name".*?<a.*?>'
                       r'(.*?)</a>.*?class="star">(.*?)</p>.*?class='
                       r'"releasetime">(.*?)</p>.*?class="integer">(.*?)</i>'
                       r'.*?class="fraction">(.*?)</i>',re.S)
    results=re.findall(pattern,html)#提取信息
    for r in results:
        string = r[0]+','+r[1]+','+r[2].strip()[3:].replace(',','/')+','+r[3][5:]+','+r[4]+r[5]+'\n'
        f.write(string)#保存

#主体函数
def main():
    if not os.path.exists('data'):#判断文件是否存在
        os.mkdir('data')#如果不存在，则创建文件夹
    f = open('data/movies.csv','w')
    f.write('图片链接,电影,主演,上映时间,评分\n')#加入第一行对应的信息
    for i in range(10):#翻页
        url='https://maoyan.com/board/4?offset='+str(i*10)#url
        html=get_response(url)#获得响应
        get_info(html,f)#提取信息
    f.close()

if __name__=='__main__':
    main()
