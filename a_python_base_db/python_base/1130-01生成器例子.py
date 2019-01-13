# coding=utf-8
# author = cjb

# ****************************生成器例子***********************************
arr = (x for x in range(1, 5))
print(arr)
for i in arr:
    print(i)

# print(next(arr))

print('*****************************')

arr2 = (x for x in range(1, 4))
print(next(arr2))
print(next(arr2))
print(next(arr2))
# print(next(arr2)) #报错

print('*****************************')


def test():
    n = 1
    print('first!')
    yield n
    n += 1
    print('second!')
    yield n
    n += 1
    print('third!')
    yield n


a = test()
print("next one")
print(next(a))

print("next one")
print(next(a))

print("next one")
print(next(a))

# print("next one")     # 程序出错
# print(next(a))



