#coding=utf-8
class Test:
    a=100                       #类的属性
    def __init__(self,b):
        self.b = b              #实例属性

t =  Test(898)  #实例化对象
#通过实例化对象访问类的属性
print('t.a=%d'%t.a)
#通过类名访问类的属性
print('Test.a=%d' %Test.a)
#通过实例化对象访问实例属性
print('t.b=%s' %t.b)
#通过类名访问实例属性--访问失败，不能这么访问
# print('Test.b=%s'%Test.b)
#注意：无法通过类名.属性来访问实例属性
#注意：对于类的属性我们可以通过类名及实例对象去访问



#*************************类的私有化属性*********************
"""
学习目标
掌握类的私有化属性

课程内容
a.私有化属性的表示方法
b.访问私有化属性的方法
c.注意事项
"""

# a.私有化属性的表示方法
class student():
    def __init__(self):
        self.__number = 30

banji =  student()
print(banji.__number)  #访问失败


# b.访问私有化属性的方法--在类的内部访问
class student4():
    def __init__(self, num):
        self.__number = num
    def print_name(self):
        print('age is %d'%self.__number)

age =  student4()
age.print_name()


# c.注意事项
# python中没有c++，java等private，public这种关键字区分共有属性还是私有属性，私有化属性以__开头，否则为公有属性
