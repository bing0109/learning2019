# coding=utf-8
# author = cjb

"""
输入和输出

课程内容
a.输出应用场景
b.输入应用场景
c.输出
d.输入


a.输出应用场景
1.taobao中搜索出来的商品
2.访问页面不存在(404)
3.调试程序时候进行输出
4.网站用户名提示等信息

b.输入应用场景
1.注册用户时候添加信息
2.taobao搜索框中输入信息
3.前后端交互

c.输出
1.直接输出
2.变量输出
3.变量操作后输出
4.函数输出
5.格式化输出

d.输入
input	    python2版本中作用是接受键盘输入的数字信息，python3中作用是接受键盘输入的字符串信息
raw_input 	python2中接受键盘输入字符信息，python3中已经取消
注意：NameError: name 'raw_input' is not defined

"""

#直接输出 是通过print()函数进行打印
print('abc!')

#变量输出
a = 'python'
b = input('please input str:')
print(a)
print(b)

#变量操作后输出
print(a+b)

#函数输出
print(abs(-9))

#格式化输出
# %s 输出字符串
# %d 输出整型

name=input('请输入您的大号：')
age=int(input('请输入您的年龄：'))
print('your name is %s, age is %d' %(name, age))

# 补充：数据类型转换   int() 转换为整型 str（）转换为字符串



