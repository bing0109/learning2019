#!usr/bin/env python
# _*_ coding:utf-8 _*_

# 用python打印出9*9乘法口诀表

i = 1
j = 1

for i in range(1, 10):
    for j in range(1, 10):
        if i >= j:
            print('%d*%d = %d' % (j, i, i*j), end=', ')
            j += 1
    print('\r')
    i += 1


