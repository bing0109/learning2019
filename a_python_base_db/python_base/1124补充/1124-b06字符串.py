# coding=utf-8
# author = cjb
"""
学习目标
掌握字符串常见操作

课程内容
a.字符串的应用场景
b.字符串的索引
c.字符串的切片
d.其他操作
e.引号



a.字符串的应用场景
	1.用户名、密码、邮箱
	2.电话号码升级
		0452-8869504
		0452-68869504
	3.爬虫网站域名
		www.baidu.com--->baidu
		www.acfun.com--->acfun
	4.分词
		hello im your baba
		你猜不猜我猜你猜我不猜
	5.密码破解
	6.报告

b.字符串的索引
	索引：下标，从0开始，可以从左到右，也可以从右到左
	字符串可以通过string[x]，x作为索引进行字符串的截取
	b   a   i   d   u
	0   1   2   3   4
	-5  -4  -3  -2  -1
	注意：IndexError: string index out of range 索引超出范围

c.字符串的切片
	切片：通过索引截取所需要的信息，截取的信息是x,y-1

d.其他操作
	a.拼接
	b.遍历
	c.去空格
	d.计算长度
e.引号
	1.单引号
	2.双引号
	3.三引号


1.
    1. 提示用户输入内容，如果为空则提示！
    2. 判断用户输入的字符串首字母是否为元音（A、E、I、O、U）
    3. 如果为元音，则在字符串后加上'ay'
        eg. 如果用户输入'apple'->'appleay'
    4. 如果首字母为辅音字母，则将该字符串首字母移动结尾，并加上'ay'
        eg. 如果用户输入'hello'->'ellohay'。
2.输入两个字符串，从第一字符串中删除第二个字符串中所有的字符。
#例如，输入”They are students.”和”aeiou”，则删除之后的第一个字符串变成”Thy r stdnts.”
修改后：输出被删除后的第一个字符串的值
"""
a = "baidu.com"

#索引
print(a[0])
print(a[-5])

#切片
print(a[2:3])
print(a[4:])
print(a[:3])
print(a[2:-3])
print(a[:-4])
print(a[:])
print(a[::-1])  # 字符串翻转
print(a[3::-1])  # 字符串翻转，并截取部分

#拼接
a = '   baid  u.com  '
b = ' h ttps '

print(a+b)
print(a[:-4]+b[3])

#遍历
for i in a:
    print(i)


#成员运算
if "d" in a:
    print('d is here')


#去掉空格
print(a.strip())	    #去掉左右空格
print(a.lstrip())    #去掉左边空格
print(a.rstrip())    #去掉右边空格
print(a.strip('0'))     #移出字符串左右两侧的指定字符‘0’

#计算长度
print(len(a))

#切片
print(a.split())        # 默认以空格进行切片
print(a.split('.'))     # 以 . 进行切片



"""
#课后左右1
1.
    1. 提示用户输入内容，如果为空则提示！
    2. 判断用户输入的字符串首字母是否为元音（A、E、I、O、U）
    3. 如果为元音，则在字符串后加上'ay'
        eg. 如果用户输入'apple'->'appleay'
    4. 如果首字母为辅音字母，则将该字符串首字母移动结尾，并加上'ay'
        eg. 如果用户输入'hello'->'ellohay'。
2.输入两个字符串，从第一字符串中删除第二个字符串中所有的字符。
#例如，输入”They are students.”和”aeiou”，则删除之后的第一个字符串变成”Thy r stdnts.”
修改后：输出被删除后的第一个字符串的值
"""
#1
input1 = input("please in put a string:")

if input1 is None:
    print("please input string!")

if input1[0] in ['A','E','I','O','U']:
    print(input1 + 'ay')

else:
    print(input1[::-1] + 'ay')


#2
a = input("please in put a string1:")
b = input("please in put a string2:")
for i in b:
    if i in a:
        a = a.replace(i, '')

print(a)




