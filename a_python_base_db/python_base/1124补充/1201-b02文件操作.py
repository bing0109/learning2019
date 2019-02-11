学习目标
掌握文件操作基本方法

课程内容
a.文件操作的应用场景
b.文件操作实例
c.read readline readlines区别
d.csv文件操作


a.文件操作的应用场景
	1.网站记录日志的时候
	2.报表数据
	3.爬虫爬取的数据写入文件
	4.招聘网站简历的导入导出


b.文件操作实例
    1.读文件
        注意，open函数参数的第一个是文件的路径，第二个是对应的操作
            r表示读
            w表示写
            a表示追加内容
            b表示以二进制操作，例如rb wb ab
            
        f = open('/home/bing/abc.txt', 'r')
        for i in f:
            print(i)
            
        f.close()
        
    2.写文件
        只能写入字符串，如果没有该文件，就自动创建
        str1 = 'hello world'
        f = open('/home/bing/abc.txt', 'w')
        f.write(str1)
        f.close()
        
    3.追加内容
        注意：注意要换行，\n
        f = open('/home/bing/abc.txt', 'w')
        f.write('\n world')
        f.close()
            
            
            
c. read readline readlines区别
    
    read        读取整个文件
    readline    读取下一行
    readlines   读取真个文件到一个迭代器用于遍历每一行
    

d. csv文件操作
    csv文件是什么
	    逗号分割值，文件以纯文本形式存储表格数据

    csv文件读写
        1.csv文件的读
            注意：导入模块（自带），
            import csv
            with open('/home/1.csv', 'r') as f:
                reader = csv.reader(f)
                for i in reader:
                    print(i)
                    
        2.csv文件的写入
            注意：python生成的csv文件要被excel兼容的话，必须带有参数dialect='execl'
            with open('/home/2.csv', 'w') as f:
                file = csv.writer(f, dialect='excel')
                file.writerow([1,2,3,4])
                file.writerow([5,6,7,8])


































