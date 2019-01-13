#coding=utf-8
"""
a.__init__()使用方法
用于定义默认值
class 类名：
    def __init__(self):
        方法列表
    
b.__init__()调用    
"""


class student:
    def __init__(self):
        self.boy = 20
        self.girl = 30
    def study(self):
        print('good study')

simida =  student()  # 实例化对象
print(simida.boy)
print(simida.girl)
# 注意：没有创建对象的时候没有调用__init__()方法前就默认有2个属性，一个boy，一个gir，__init__()方法在创建对象后立刻被默认调用

class student1():
    def __init__(self, boy, girl):
        self.badboy = boy
        self.cutegirl = girl
    def study(self):
        print('study')

z = student1(40,70)
print('有男生%d个'%z.badboy)
print('有女生%d个'%z.cutegirl)

"""
c.补充内容：
__init__()方法，创建一个对象时被默认调用，不需要手动调用
__init__(self)中第一个参数的名字是self，如果在创建对象时传递2个实参，在__init__(self)中还需要2个额外的实参
"""


print('**************************************************')
class Student2:
    def __init__(self, name):
        self.name = name

    def info(self):
        print('name is %s' %self.name)


def studentinfo2(s):
    s.info()

h1 = Student2('ladygaga')

# h1是student类的实例化对象
# 对象实例化之后可以使用类的方法
print(h1.name)
studentinfo2(h1)
# studentinfo2括号中传入的h1是一个经过实例化的对象调用类的方法
# 注意：函数传参可以传入常规函数，也可以传入对象
print('******************************')
h2 = Student2('python')
h2.info()

print(h2.info())  # 这个会多打印出一个None出来，在类里面已经打印了，不用重复打印一次
