#!usr/bin/env python
# _*_ coding:utf-8 _*_

学习目标
掌握多进程的常规操作


课程内容
a.multiprocessing(多进程)
b.添加进程
c.进程锁


a.multiprocessing(多进程)
    作用：弥补threading中的gil问题（同一时间只能有一个线程运行的问题（伪并发））


b.添加进程
    注意：运用的时候要加一个定义man函数的语句

    if __name__=='__main__'
    注意：上述代码在python中有2中使用方法
        1.作为脚本运行
        2.作为模块运行

    if __name__=='__main__'的作用是控制代码的执行过程，在...下面的代码只有作为脚本运行的时候才能执行，如果作为模块运行，就不被执行


    import multiprocessing as mp

    def job(a,d):
        print(a+d)


    if __name__ =='__main__':
        p1 = mp.Process(target=job,args=(2,4))      # 添加进程
        p1.start()
        p1.join()


c.进程锁
    解决不同进程间资源共享的问题，用进程锁解决















