from urllib import request, parse, error
import requests
print('-----------------------urlopen get--------------------------')

# urllib.request.ulropen
# # get请求
# res1 = request.urlopen(url='http://httpbin.org/get')
# print(res1)             # 返回一个对象
# print(res1.headers)     # 输出消息头里面的内容
# print(res1.headers['Date'])     # 输出消息头里面的内容的具体字段
# print(res1.read())      # 读取返回的内容
#
# try:
#     res1 = request.urlopen(url='http://httpbin.org/get', timeout=0.1)
# except error.URLError as e:
#     print(e)

print('-----------------------urlopen post--------------------------')

# # post请求
# data = {
#     'hello': '人工智能',
#     'wd': 'python'
# }
# # POST发送的data必须为bytes或bytes类型的可迭代对象，不能是字符串
# data1 = bytes(parse.urlencode(data), encoding='utf-8')
# res2 = request.urlopen('http://httpbin.org/post', data=data1)
# # print(res2)             # 返回一个对象
# # print(res2.headers)     # 输出消息头里面的内容
# # print(res2.headers['Date'])     # 输出消息头里面的内容的具体字段值
# # print(res2.getheaders())            # 输出消息头，字典格式
# # print(res2.getheader('Server'))       # 输出消息头中Server的值
# # print(res2.read().decode('utf-8'))      # 读取返回的内容，中文还是显示位编码格式，可以提取出来之后再转换
# # print(res)

#
# print('-----------------Request-------------------------')
#
# # urllib.request.Request
# req_header = {
#     "referer": 'fanyi.youdao.com',
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
# }
# form_data = {
#     'hello': '人工智能',
#     'wd': 'python'
# }
#
# print('-----------------Request-post------------------------')
# # post发送的date必须是bytes或byte类型的可迭代对象，不能是字符串
# form_data = bytes(parse.urlencode(form_data).encode('utf8'))
# # 构造请求对象Request
# req3 = request.Request(url='http://httpbin.org/post', data=form_data, headers=req_header, method='POST')
# req3.add_header('User-Agent', 'nimei')  # 添加header参数，之前存在，会覆盖之前的
# req3.add_header('abced', 'yuiop')       # 添加header参数，之前不存在，会追加
# res3 = request.urlopen(req3)
# print(res3.read().decode('utf8'))
#
# print('-----------------Request-post-no data------------------------')
# req4 = request.Request(url='http://httpbin.org/post', data=None, headers=req_header, method='POST')
# res4 = request.urlopen(req4)
# print(res4.read().decode('utf8'))
#
# print('-----------------Request-get------------------------')
# req5 = request.Request(url='http://httpbin.org/get', data=None, headers=req_header)
# res5 = request.urlopen(req4)
# print(res5.read().decode('utf8'))


print('-----------------requests------------------------')
print('-----------------requests-get-----------------------')
params = {
    'wd': '人工智能',
    'hello': 'world'
}
url = 'http://httpbin.org/get'
res6 = requests.get(url=url, params=params)
print(type(res6))
print(res6.cookies)
print(type(res6.status_code), res6.status_code)
print(res6.text)     # 返回响应对象，主要用于获取文本
print(res6.content, 'utf8')  # 返回响应对象，结果前带有一个b，这代表是bytes类型的数据，主要用于获取 图片、文件等
# 参考 https://www.jianshu.com/p/d7ca8f0a2641


print('-----------------requests-post-----------------------')
params = {
    'wd': '人工智能',
    'hello': 'world'
}
url = 'http://httpbin.org/post'
data = {
    'abc': '爬虫',
    'def': 'scripy'
}
file = {'file': open('test.txt', 'rb')}
headers = {
    'Cookie': 'cna=llA7E8brPBoCAbcOHNi7hVAV; enc=ccE6LTKXBdwRHQ7N5jkpqIncgJ8Z',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53"
}

s = requests.Session()
res7 = s.post(url=url, data=data, params=params, files=file, headers=headers)
print(res7.text)
