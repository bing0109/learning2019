#coding=utf-8
"""
1.设计一个计算器，输入数字1，数字2和运算符号。输出其计算结果
2.通过自定义函数方式实现以上功能
3.通过有参数有返回值方式实现以上功能 
"""

num11 = input("请输入数字1：")
num22 = input("请输入数字2：")
method1 = input("请输入运算符：")

def calculator(num1, num2, method):
    if num1.isdigit() is False:
        return print("please input num1 number type")
    
    if num2.isdigit() is False:
        return print("please input num2 number type")

    if num1.isdigit() is True and num2.isdigit() is True:
        if method == "+":
            return int(num1) + int(num2)
        
        elif method == "-":
            return int(num1) - int(num2)
        
        elif method == "*":
            return int(num1) * int(num2)
        
        elif method == "/":
            return int(num1) / int(num2)

        else:
            return print('please input the right operator')

print('计算结果为：', calculator(num11, num22, method1))

#test