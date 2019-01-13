学习目标
    掌握生成器的概念
    
课程内容
    a.生成器是什么？
    b.生成器实例
    c.注意事项
    
    
    
a.生成器是什么？
    generator列表生成器:
    用来替代"不一定使用全部元素的数组"而是要使用的时候才生成该元素，用来节省空间


b.生成器实例
    eg1:
    arr = (x for x in range(1,5))
    print(arr)  #这么打印出来是一个对象
    for i in arr:
        print i     # for循环调用arr，打印出1、2、3、4
        
     print(next(arr))   #程序出错，提示已停止循环，因为上面的for循环已经用完了
        
    eg2:
    arr = (x for x in range(1,5))
    print(next(arr))        #打印出：1
    print(next(arr))        #打印出：2
    print(next(arr))        #打印出：3
    print(next(arr))        #打印出：4
    print(next(arr))        #提示stopinteration

    
    eg3：
    def test():
        n=1
        print('first!')
        yield n
        n += 1
        print('second!')
        yield n
        n+=1
        print('third!')
        yield n
    
    a = test
    print('next one')
    print(next(a))
    
    
c.注意事项
    生成器是一种特殊的迭代器，它的返回值不是通过return，是通过yield每次调用next()，计算出下一个元素的值，直到最后一个元素，如果没有更多元素会提示stopinteration

    生成的是一个对象，不会把数据直接创建出来，当for遍历的时候，生成器对象会调用next()函数，获取下一个要生成的数据
    
    生成式对象可以调用next()函数获取下一个要生成的数字,如果next(）函数没有获取到下一个数据，会抛出异常StopIteration ,程序出错
    生成式对象可以使用for遍历，使用next()不停的获取下一个数据，如果没有下一个数据循环结束
    列表生成式： 会将所有的结果全部计算出来，把结果存放到内存中，如果列表中数据比较多，会占用过多的内存空间，可能导致MemoryError内存错误或者导致程序在运行时出现卡顿的情况 
    列表生成器：会创建一个列表生成器对象，不会一次性的把所有结果都计算出来，如果需要序号获取数据，可以使用next（）函数来获取，但要注意，一旦next()函数获取不到数据，会导致出现StopIteration异常错误，可以使用 for循环遍历生成器对象，获取所有数据 
    视情况而定，如果数据量比较大，推荐使用生成器； 

















