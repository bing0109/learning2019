# 学习目标
# 掌握 类的方法 的定义
#
# 课程内容
# a.类的方法的定义
# b.类的方法实例

# a.类的方法的定义
# 类的方法，对应的函数不需要实例化,通常用装饰器@classmethod来标识方法，对于类的方法，第一个参数必须是类的对象，一般以cls作为第一个参数。可以通过实例化对象和类对象进行访问

# 静态方法，@staticmethod
    # 不能访问实例属性，参数不能传入self！
    # 与类相关但是不依赖类与实例的方法！



# b.类的方法-实例
class people:
    country = 'china'
    @classmethod
    def getcountry(cls):
        return cls.country

    @classmethod
    def setcountry(cls,country):
        cls.country = country

p = people()
print(p.getcountry())           # 通过实例对象调用类的方法
print(people.getcountry())      # 通过类对象调用的方法

print('*********************************')
# 类的方法还有一个用途是可以对类的属性进行修改
p1 = people
print(p.getcountry())
p.setcountry('usa')
print(p.getcountry())


print('*********************************')


class A():
    # 属性默认为类属性（可直接被类本身调用）
    num = '类属性'

    # 实例属性
    def __init__(self, a):
        self.a = '实例属性' + str(a)
        self._b = '私有属性,单下划线_开头，外部依然可以访问更改'
        self.__c = '私有属性，双下划线__开头：外部不可通过instancename.propertyname来访问或者更改'

    # 实例化方法（必须实例化类后才能被调用）
    def func1(self):  # self表示实例化类后的地址id
        print('实例化方法func1')
        print(self.a)

    # 类方法（不需要实例化类就可以被类本身调用）
    @classmethod
    def func2(cls):  # cls表示没有被实例化的类本身
        print("类方法func2")
        print(cls)
        print(cls.num)
        # cls().func1()

    # 不传递默认self参数的方法（该方法也是可以直接被类掉用，但这么做不标准）
    def func3():
        print('func3')
        print(A.num)  # 属性是可以直接用类本身调用的

    # 静态方法
    @staticmethod
    def fun4():
        print()


# A.func1() 这样调用是会报错：因为func1()调用时需要默认传递实例化类后的地址id参数，如果不实例化类是无法调用的
shili = A('实例属性a')
shili.func1()
print(shili._b)  # 单下划线私有属性的访问方法
print(shili._A__c)  # 双下划线私有属性其实还是可以访问的
print('*********************************')
A.func2()
print('*********************************')
A.func3()





# 总结：类属性与类方法是类固有的方法与属性，不会因为实例不同而改变，写他们的目的是减少多实例时所创造出来的内存空间，加快运行速度。