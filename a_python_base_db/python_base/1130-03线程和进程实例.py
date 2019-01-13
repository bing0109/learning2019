#!usr/bin/env python
# _*_ coding:utf-8 _*_

import threading
import time

print(threading.active_count())
print(threading.current_thread())

print('*********************************************************')


def thread_job1():
    print('当前线程1是%s' %threading.current_thread())


def thread_job2():
    print('当前线程2是%s' %threading.current_thread())


thread1 = threading.Thread(target=thread_job1())
thread2 = threading.Thread(target=thread_job2())
thread1.start()
thread2.start()


print('*********************************************************')


def t1():
    print('t1开始了')
    # for i in range(10):
    #     time.sleep(0.1)
    print('t1结束了')


def t2():
    print('t2开始了')
    print('t2结束了')


th1 = threading.Thread(target=t1)
th2 = threading.Thread(target=t2)
th2.start()
th1.start()
th1.join()
th2.join()
print('finish')


print('*********************************************************')


# 线程锁--效果不太明显
def job1():
    global a, lock
    lock.acquire()
    for i in range(10):
        a += 1
        print('job', a)
    lock.release()


def job2():
    global a, lock
    lock.acquire()
    for i in range(10):
        a += 10
        print('job2', a)
    lock.release()


lock = threading.Lock()
a = 0
th1 = threading.Thread(target=job1)
th2 = threading.Thread(target=job2)
th1.start()
th2.start()
th2.join()
th1.join()


# print('*********************************************************')


