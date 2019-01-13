#coding=utf-8

# 不定长传参--*arg传入的是元组
def animal(pet1, pet2, *args):
    print(pet1, pet2, args)

animal('dog', 'cat', 'abc', 'drf')

print('********************************************')
#不定长传参--**arg传入的是字典
def animal1(pet1, pet2, **args):
	print(pet1, pet2, args)

animal1('dog','cat',a='abc',b='drf')




dic={'name':'abcdef', 'tel':119}
print(dic)
print(dic.keys())
print(dic.values())
print(dic.items())




a = 100
def test1():
    a = 20
    print('test1中a的值：', a)

def test2():
	print('test2中a的值：', a)

def test3():
	global a
	a = 200
	print('test3中a的值：', a)

def test4():
	print('test4中a的值：', a)

test1()
test2()
test3()
test4()





