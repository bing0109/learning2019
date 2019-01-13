#coding=utf-8
"""
装饰器
重点--必问题

学习目标
掌握装饰器写法及作用

课程内容
a.装饰器
b.装饰器例子


a.装饰器
在不修改原来函数代码的情况下，给函数赋予新的功能

例子
银行转账：
    A--转账--B
    1.A账户中减少金额
		用装饰器 增加写入日志功能(记录什么时间，哪个账户，什么操作)
	2.B账户中增加金额
		用装饰器 增加写入日志功能(记录什么时间，哪个账户，什么操作)

"""

#b.装饰器例子
import time

#计算函数运行时间
def jisuan(func):
    def zhshiqi():
        stime = time.time()
        func()
        etime = time.time()
        print('process time = %s second' %(etime - stime))
    return zhshiqi

@jisuan
def func():
    print('hello')
    time.sleep(1)
    print('world')

func()

print('**********************************************************')


# 补充，带参数的装饰器
def dec(func1):
    def jisuan(a, b):  # 装饰器中的参数数量必须要和被装饰的函数一致
        stime = time.time()
        func1(a, b)
        etime = time.time()
        sec = etime - stime
        print('process time is %d s' %sec)
    return jisuan

@dec
def func1(a, b):
    print('a+b=?')
    time.sleep(1)
    print('its', a+b)

func1(4, 5)
