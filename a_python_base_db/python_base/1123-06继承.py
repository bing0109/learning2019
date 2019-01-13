"""学习目标
掌握继承定义和使用方法

课程内容
a.单继承
b.多继承
c.父类重写
"""

class A():
    def printa(self):
        print('-----------a---------')

class B():
    def printb(self):
        print('-----------b---------')

#a.单继承
#一个类派生另一个子类，子类继承父类的属性和方法
class C1(A):
    def printc1(self):
        print('----------C1--------')

cc1 = C1()
cc1.printa()
cc1.printc1()

#b.多继承
#子类继承多个父类的属性和方法
class C2(A, B):
    def printc2(self):
        print('----------C2--------')

cc2 = C2()
cc2.printa()
cc2.printb()
cc2.printc2()


#c.父类重写
#当子类中方法和父类中方法名字一致的时候，子类会重写父类
class C3(A):
    def printc3(self):
        print('----------C3--------')

    def printa(self):
        print('-----------aC3---------')

cc3 = C3()
cc3.printa()
cc3.printc3()