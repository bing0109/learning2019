#!usr/bin/env python
# _*_ coding:utf-8 _*_

# def fab(max):
#     a, b, n = 0, 1, 1
#     while n < max:
#         a, b = b, a+b
#         n += 1
#         yield b
#
#
# f = fab(6)
#
# print(f.next())
#


us_pw = {'abc': '123', 'dev': '456'}

while True:
    user = input('please input user name:')
    if user not in us_pw.keys():
        print('please input the right user name!')
        continue
    else:
        pw = input('please input password:')
        if pw == '':
            print('password cannot be null!')
            break

        elif us_pw[user] != pw:
            print('username and pw not match, please input again!')
            break

        elif us_pw[user] == pw:
            print('congratuations,username match the pw!')
            break

