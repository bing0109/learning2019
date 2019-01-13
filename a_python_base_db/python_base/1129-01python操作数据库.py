#!usr/bin/env python
# _*_ coding:utf-8 _*_

课程目标
掌握python操作数据库的方法

可能内容
a.python 操作 mongodb数据库
b.python操作 myqsl数据库



a.python 操作 mongodb数据库
	1.使用python操作数据库必须安装对应的模块
		#pymongo是python操作mongodb数据库的模块
		
		sudo pip3 install pymongo
	
	2.程序代码如下：
		import pymongo
		#设置链接参数
		conn = pymongo.MongoClient(host='127.0.0.1', port = 27017)
		db = conn.test
		db.xiyouji.insert({name:'heygor'})
		
	

b.python操作 myqsl数据库
	1.安装模块
		a.通过pip安装
			sudo pip3 install pymysql
		b.通过压缩包安装
		
	2.操作数据库
	import pymysql
	conn = pymysql.connect(host = 'localhost',user='root',passwd='root',db='sakila',port=3306,charset='utf8')
    	#host		连接数据库所在服务器的ip
		#user		数据库的用户名
		#passwd		数据库的密码
		#db			数据库名称
		#port		数据库端口
		#charset	字符集
	cur = conn.cursor()		#定义游标
	cur.execute('select * from city')	#所需指定的语句
	data = cur.fetchall()	#获取语句执行的结果
	for i in data:
		print(i)
	
	cur.close()		#关闭游标
	conn.close()	#关闭连接，释放数据库资源
	
	
	
	
	
	






