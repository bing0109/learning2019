# coding=utf-8
# author = cjb

"""
学习目标
掌握循环的操作

课程内容
a.循环的使用场景
b.python中的循环分类
c.for循环
d.while循环
e.跳出循环


a.循环的使用场景
	1.输入密码次数不能超过3次
	2.不输入正确付款码不能进行下一步
	3.爬虫解析页面从头到尾
	4.重复利用资源

b.循环的分类
	1.for循环
	2.while循环
	3.跳出循环

c.for循环
可以遍历任何序列的项目，比如一个列表、一个字符串等等
	for 变量 in 列表，元组，字典，函数:
		执行语句

d.while循环
while循环后面判断条件只能是真或者假，如果为真，继续运行，如果为假，不执行
	while	判断条件:
		执行语句

e.跳出循环
	continue	跳出本次循环
	break		跳出整个循环
	注意：冒号和缩进，python中没有do while循环
"""


#coding=utf-8
str1='python is no.1'
for i in str1:
	print(i)
#补充：空格也是字符串

li=['5kong','8jie','shasir']
for i in li:
	print(i)

#函数range()
#range(10)	从0开始，0-9
#range(1,10)	从1开始，1-9

for i in range(10):
    print(i)

for i in range(1,10):
    print(i)




a = 0
while a<10:
    a += 1
    if a == 6:
        # continue
        break

    print('i am :', a)
