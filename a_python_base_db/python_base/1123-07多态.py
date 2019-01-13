#coding=utf-8
# 学习目标
# 掌握多态的概念
#
# 课程内容
# a.什么是多态
# b.多态的例子

# a.什么是多态
#多态：多种形态，一个方法能表现出不同的形态，同一操作方法针对不同对象，有不同的解释，产生不同的结果

#：多态的实现
a=20
b=10
print(a+b)
a='heygor '
b='shuai'
print(a+b)

class animal:
    def jiao(self):
        print('ao~~~~~~')

class dog(animal):
    def jiao(self):
        print('汪！！！！')

class cat(animal):
    def jiao(self):
        print('miao~~~~~')

def test(s):
    s.jiao()

a=animal()
a.jiao()
b=dog()
c=cat()
test(b)
test(c)










