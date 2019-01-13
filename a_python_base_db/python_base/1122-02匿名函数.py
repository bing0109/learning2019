#coding=utf-8
#匿名函数lambda
#例子：字典排序
stu=[{'name':'pig','age':18},{'name':'dog','age':3},{'name':'cat','age':30}]
stu.sort(key=lambda x:x["age"])
print(stu)

print("*********************************************************************************")

def operation(a,b,opt):
    re = opt(a,b)
    return re

num1 = 1
num2 = 3
res = operation(num1,num2,lambda a,b:a+b)
print(res)


def lambda1(a,b):
    return a+b

abc = lambda1(12,13)
print(abc)
