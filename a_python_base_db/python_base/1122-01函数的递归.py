#coding = utf-8
#函数递归
def func(n):
    print('进入第%d层梦' %n)
    if n == 3:
        print('进入潜意识区')
    else:
        func(n+1)
    print('从第%d层梦中醒来' %n)


func(1)