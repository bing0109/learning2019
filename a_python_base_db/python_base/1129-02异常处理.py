#!usr/bin/env python
# _*_ coding:utf-8 _*_
"""
学习目标
    掌握异常处理的机制和方法
    
课程内容
a.异常的概念
b.常见的异常
c.异常的处理方式



a.异常的概念
    程序执行过程中发生影响程序正常运行的事件，当python无法正常处理的时候会产生异常
    异常时python中的一个对象，表示一个错误
    
    捕获异常：为防止python程序终止，当脚本发生异常的时候，需要进行捕获


b.常见的异常
    1.NameError
        没定义变量就直接使用
        
    2.SyntaxError
        语法错误
    
    3.IO Error
        FileNotFoundError
#            >>> p = open('/home/cbd.a')
            Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
            FileNotFoundError: [Errno 2] No such file or directory: '/home/cbd.a'
#            >>>
            
    4.ZeroDvisionError
        除数为0
#            >>> 1/0
            Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
            ZeroDivisionError: division by zero
#            >>>
            
    5.ValueError
        值有问题
#            >>> int('a')
            Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
            ValueError: invalid literal for int() with base 10: 'a'
#            >>>



c.异常的处理方式
    用的最多的是1、3，第5个基本没人用

    1. try ... except
        有可能发生错误的代码放在try和except中间
        例子：
            try:
                j
            except NameError as e:
                print('catch error!')
                
                
    2.try ... except ... else
        语法：
        try:
            codes
        except:
            codes
        else:
            codes
            #如果没有报错可以执行的其他操作
            
    
    3.try ... finally
        语法：
        try:
            codes
        finally:
            codes
            #如果没有捕获到异常，代码执行
            #如果捕获到异常，先执行代码，然后出来异常，finally后面的代码一定会执行
    
            
    4.try ... except ... finally
        语法：
        try:
            codes
        except:
            codes
        finally:
            codes
            # 如果try没有捕获到异常，那么执行finally语句
            # 如果try捕获到异常，先显示异常，再执行finally
          
        
    5.try ... except ... else ... finally
        基本没人用



"""
import datetime

try:
    abs('g')
except TypeError as e:
    print('get nameError')
    print(datetime.datetime.now().strftime('%Y-%m-%D %H:%M:%S'), e)
finally:
    print('print finally')

















