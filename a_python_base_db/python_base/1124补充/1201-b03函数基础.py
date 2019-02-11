一、函数的定义和调用
    课程目标
    掌握函数定义和调用的方法

    课程内容
    a.什么是函数
    b.函数的定义
    c.函数的调用


    a.什么是函数
    开发后需要使用指定代码多次，为了提高代码效率和重用性，所以把具有独立功能的代码组织为一个模块，
    给这个功能一个名字，就是函数
    函数可以使用系统自带函数，也可以使用自定义函数

    例子：登录网站
    1.打开网页
    2.点击用户名输入框
    3.清空用户名输入框
    4.输入用户名信息
    5.点击密码输入框
    6.清空密码输入狂
    7.输入密码信息
    8.点击登录

    [1]
    1.打开网页
    2.输入用户名信息
	    点击XX
	    清空XX
	    填写XX
    3.输入密码信息
	    点击XX
	    清空XX
	    填写XX
    4.登录
    [2]
    定义一个函数
    函数的功能：输入信息(信息类型，信息)
    信息类型：用户名  密码
    信息：	  根据实际情况填写
    定义函数：
    输入信息(信息类型，信息)
	    点击 信息类型 输入框
	    清空 信息类型 输入框
	    填写 信息
    1.打开网页
    2.调用函数输入信息(用户名，osimeno)
    3.调用函数输入信息(密码，123456)
    4.点击登录

    b.函数的定义
	    语法：
		    def 函数名字():
			    函数的主体
	    例子：
		    def print_name():
			    print('this is heygor!')

    c.函数的调用
	    1.调用自定义函数
	    函数名
	    2.内置函数调用
	    内置函数可以直接使用，调用一个函数需要函数名字，函数参数，函数名字是一个函数对象的引用，可以把函数赋值给变量



二、函数的常用格式
    学习目标
    掌握函数的常用格式

    课程内容
    a.函数的常用类型
    b.常用类型实例



    a.函数的常用类型
	    1.无参数，无返回值(自己工作，散养)
	    2.无参数，有返回值(主动发周报)
	    3.有参数，无返回值(领导安排任务，不管效果)
	    4.有参数，有返回值(领导安排任务，要求汇报任务完成情况)

    b.常用函数类型实例
	    #1.无参数，无返回值
	    def print_hello():
		    print('hello world!')

	    print_hello()
	    #2.无参数，有返回值
	    def sleep():
		    return 'sleep'

	    s=sleep()
	    print(s)
	    #3.有参数无返回值
	    def sub(x,y):
		    print('x+y=',x+y)
	    sub(2,3)
	    #4.有参数有返回值
	    def sub(x,y):
		    return x+y
	    res=sub(20,30)
	    print(res)

三、函数的的返回值
    学习目标
    掌握函数返回值的用法

    课程内容
    a.返回值的定义
    b.return和print区别
    c.return语句

    a.返回值的定义
    函数定义时候是直接输出，有时候需要处理一些函数，根据参数进行一些操作，需要返回值

    b.return和print区别
    return的作用是返回计算的值(结果)，需要print才能打印出来
    print作用是输出数据到控制端


    c.return语句
    用于退出函数，return下面的语句是不会执行的
    一个返回值
    def sum(a,b):
            jisuan=a+b
            return jisuan
    s=sum(20,30)
    print(s)
    多个返回值
    def re(a,b):
            a*=10
            b*=10
            return a,b
    num=re(4,5)
    print(num)
    print(type(num))

    num1,num2=re(10,50)
    print(num1,num2)

    1.设计一个计算器，输入数字1，数字2和运算符号。输出其计算结果
    2.通过自定义函数方式实现以上功能
    3.通过有参数有返回值方式实现以上功能



四、函数的参数传递
    学习目标
    掌握函数参数传递的方法

    课程内容
    a.函数的形参和实参
    b.参数传递-实参位置
    c.参数传递-关键字参数
    d.参数传递-参数默认值
    e.参数传递-不定长参数


    a.函数的形参和实参
    def print_name(name):
	    print('hello,%s'%name)
    print_name('o8ma')

    例子中形参为定义函数括号中的name，实参是调用函数时候传入的o8ma
    定义在函数体内参数是形参，调用时候传入参数是实参

    b.参数传递-实参位置
    函数允许定义多个形参，可以包含多个实参，通过形参和实参对应顺序就是实参位置，只有位置一致才能匹配
    def animal(pet1,pet2):
            print(pet1+' wang!'+pet2+' miao')

    #调用函数传入两个参数
    animal('dog','cat')

    c.参数传递-关键字参数
    def animal(pet1,pet2):
            print(pet1+' wang!'+pet2+' miao')

    animal(pet2='cat',pet1='dog')

    d.参数传递-参数默认值
    函数在定义时候设置函数形参，每个形参设置一个默认值，当函数在调用的时候，如果没有实参，就是形参
    def animal(pet2,pet1='2ha'):
            print(pet1+' wang!'+pet2+' miao')

    animal('bosi')
    animal('pig','out man')

    e.参数传递-不定长参数
    有时候一个函数处理比当初声明更多的参数叫做不定长参数

    def test(x,y,*args):
            print(x,y,args)

    test(1,2,'heygor','simida')
    注意：*args位置参数传入装配为元组类型

    def test1(x,y,**args):
            print(x,y,args)

    test1(1,2,a=9,b='heygor',c=300)
    注意：**args位置参数传入装配成字典类型



五、变量的作用域
    学习目标
    掌握变量作用域概念及用法

    课程内容
    a.全局变量和局部变量
    b.局部变量
    c.全局变量


    a.全局变量和局部变量
    全局变量：定义在函数外的变量
    局部变量：定义在函数内部的变量
    获取变量值的时候，先获取当前作用域的名称和变量值，如果没有找到，到上一层作用域搜索变量的值，再没有就报错


    b.局部变量
    def test1():
            a=10
            print('修改前a的值是',a)
            a=20
            print('修改后a的值是',a)

    def test():
            a=40
            print('我是test2中的a',a)

    test1()
    test()
    注意：不同函数，可以定义相同变量的名字(局部变量)，互相不影响


    c.全局变量
    全局变量是声明在函数外的变量

    a=100
    print('a的值是',a)

    def test01():
            a=20
            print('test01中a的值是',a)

    def test02():
            print('test02中a的值是',a)

    test01()
    test02()
    补充：当局部变量和全局变量同名的时候，优先使用局部变量
    修改全局变量

    a=100
    print('a的值是',a)

    def test1():
            global a
            a=200
            print('test1中修改全局变量a',a)

    def test2():
            print('test2中使用全局变量a',a)

    test1()
    test2()



六、面向对象编程实例
    学习目标
    了解面向对象编程思路

    课程内容
    a.开车去东莞

    class road:
            def __init__(self):
                    self.juli=100
                    self.shijian=0
            def run(self,shijian):
                    self.shijian=shijian
                    if  self.shijian>60:
                            shengyu=self.juli-self.shijian*0.5
                            print('剩余距离是%d KM'%shengyu)
                            if shengyu<20:
                                    print('很快就到')
                            else:
                                    print('加了个油')
                    else:
                            print('开飞机呢？这么快！')

    print('开路！！！！')
    dongguan=road()
    #实例化对象
    print('开路20分钟')
    dongguan.run(20)
    print('开路120分钟')
    dongguan.run(120)
    print('开路160分钟')
    dongguan.run(160)
