
MongoDB
非关系型数据库
存储是以bson形式存在


a.mongodb的安装
	sudo apt-get install mongodb
	
	mongodb官网
	www.mongodb.org
	
	
b.mongodb的服务
	mongod		mongodb的主服务
	mongo		mongodb的客户端服务
	27017		mongodb的端口
	
	检查服务：
		ps -ef | grep mongod
		
	检查端口：
		netstat -an | grep 27017
		
		
c.mongodb的登录
	mongo
		登录本地test数据库
		
	mongo 127.0.0.1/admin
		登录IP为127.0.0.1的admin数据库
		
	mongo 127.0.0.1:27017/admin
		登录IP为127.0.0.1，端口为27017的admin数据库
		
		
		
d.mongodb的基础命令

	对比：	mysql		mongodb
			数据库		数据库
			表			集合
			数据		文档
		
	mongodb数据库是由集合组成
	mongodb的集合是由文档组成
	
	命令：
		db				查看当前数据库的名字
		show databases	查看当前有哪些数据库
		show dbs		查看当前有哪些数据库
		use local		数据库切换为local
		
		show tables			查看当前数据库有哪些集合
		show collections	查看当前数据库有哪些集合
		
		db.startup_log.find()	查看集合startup_log


补充：
	官网为windows下载的MSI类型包需要安装，ZIP包不用安装
	
	需把mongodb所在目录添加到 系统环境变量中
	
	Windows下面mongodb不会自动启动，需要手动命令启动
	打开命令提示符窗口
	1.在e盘创建一个文件夹data
		md e:\data
	2.输入启动命令
		mongod --dbpath e:\data --logpath e:\data\mongo.log
			其中：
				dbpath 是数据库存放路径
				logpath 是存放日子的位置
				
				

e.curd（增删改查）
	文档的新增
		与mysql不同，不需要先新增表格（集合）
		> db.xiyouji.insert({name:'tangsheng',age:88})
		WriteResult({ "nInserted" : 1 })
		>
		> db.xiyouji.insert({name:'12323dawdf'})
		WriteResult({ "nInserted" : 1 })
		>
		
	文档的查询
		> db.xiyouji.find()
		{ "_id" : ObjectId("5bfdffa469ba2ff7f00750d4"), "name" : "tangsheng", "age" : 88 }
		{ "_id" : ObjectId("5bfdffc869ba2ff7f00750d5"), "name" : "12323dawdf" }
		>
		> db.xiyouji.find({name:'tangsheng'})
		{ "_id" : ObjectId("5bfdffa469ba2ff7f00750d4"), "name" : "tangsheng", "age" : 88 }
		
			说明：_id相当于在硬盘上存储的位置
			
	
	文档的修改
		> db.xiyouji.update({name:'tangsheng'},{$set:{age:100}})
		WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
		>
		> db.xiyouji.find()
		{ "_id" : ObjectId("5bfdffa469ba2ff7f00750d4"), "name" : "tangsheng", "age" : 100 }
		{ "_id" : ObjectId("5bfdffc869ba2ff7f00750d5"), "name" : "12323dawdf" }

	
	文档的删除
		> db.xiyouji.remove({age:100})
		WriteResult({ "nRemoved" : 1 })
		>
		> db.xiyouji.find()
		{ "_id" : ObjectId("5bfdffc869ba2ff7f00750d5"), "name" : "12323dawdf" }


	
			

f.文档的新增
	新增普通文档
		> db.xiyouji.insert({name:'benbenbra'})
		WriteResult({ "nInserted" : 1 })
	
	新增文档指定_id
		> db.xiyouji.insert({_id:001,name:'tai2',age:16})
		WriteResult({ "nInserted" : 1 })
	
	新增内嵌文档
		> db.xiyouji.insert({name:'wukong',jingli:{kill:100,hit:'zhubaji'}})
		WriteResult({ "nInserted" : 1 })

	新增多个文档
		> db.xiyouji.insert([{nane:'niumowang'},{name:'tiantian'},{name:'honghaier'}])
		BulkWriteResult({
				"writeErrors" : [ ],
				"writeConcernErrors" : [ ],
				"nInserted" : 3,
				"nUpserted" : 0,
				"nMatched" : 0,
				"nModified" : 0,
				"nRemoved" : 0,
				"upserted" : [ ]
		})
		
		
		> db.xiyouji.find()
		{ "_id" : ObjectId("5bfdffc869ba2ff7f00750d5"), "name" : "12323dawdf" }
		{ "_id" : ObjectId("5bfe03b769ba2ff7f00750d6"), "name" : "benbenbra" }
		{ "_id" : 1, "name" : "tai2", "age" : 16 }
		{ "_id" : ObjectId("5bfe042769ba2ff7f00750d7"), "name" : "wukong", "jingli" : { "kill" : 100, "hit" : "zhubaji" } }
		{ "_id" : ObjectId("5bfe048369ba2ff7f00750d8"), "nane" : "niumowang" }
		{ "_id" : ObjectId("5bfe048369ba2ff7f00750d9"), "name" : "tiantian" }
		{ "_id" : ObjectId("5bfe048369ba2ff7f00750da"), "name" : "honghaier" }
		>



g.文档的删除
	删除指定文档
		> db.xiyouji.remove({name:'wukong'})
		WriteResult({ "nRemoved" : 1 })
		> db.xiyouji.find()
		{ "_id" : ObjectId("5bfdffc869ba2ff7f00750d5"), "name" : "12323dawdf" }
		{ "_id" : ObjectId("5bfe03b769ba2ff7f00750d6"), "name" : "benbenbra" }
		{ "_id" : 1, "name" : "tai2", "age" : 16 }
		{ "_id" : ObjectId("5bfe048369ba2ff7f00750d8"), "nane" : "niumowang" }
		{ "_id" : ObjectId("5bfe048369ba2ff7f00750d9"), "name" : "tiantian" }
		{ "_id" : ObjectId("5bfe048369ba2ff7f00750da"), "name" : "honghaier" }

	
	删除所有文档
		> db.xiyouji.remove({})
		WriteResult({ "nRemoved" : 6 })
		>
		> db.xiyouji.find()
		>

		


h.文档的查询
	查询所有文档内容
	db.xiyouji.find()
		> db.xiyouji.find()
		{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123, "two" : "" }
		{ "_id" : 123, "name" : "adiwnfi", "key" : "erdfi234" }
		{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "age" : 15 }
		{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "age" : 33 }
		{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 63 }
		{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 100 }
		{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 100, "date" : "2019-09-09" }
		>

	查询指定文件内容
	db.xiyouji.find({age:100})
		> db.xiyouji.find({_id:123})
		{ "_id" : 123, "name" : "adiwnfi", "key" : "erdfi234" }
		> db.xiyouji.find({name:'wukong'})
		{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "age" : 33 }
		> db.xiyouji.find({name:'shasheng'})
		{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 100 }
		{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 100, "date" : "2019-09-09" }
		>
	
	查询指定文档的指定属性
	db.集合.find({条件},{要显示的属性，0显示，1不显示，_id默认显示})
	db.xiyouji.find({age:100},{_id:0,name:1})
		> db.xiyouji.find({name:'shasheng'},{_id:0,name:1,date:1})
		{ "name" : "shasheng" }
		{ "name" : "shasheng", "date" : "2019-09-09" }
		> db.xiyouji.find({name:'shasheng'},{name:1,age:1})
		{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 100 }
		{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 100 }
		>

			

f.查询表达式
		> db.xiyouji.find()
		{ "_id" : 123, "uer" : "123", "pw" : 234 }
		{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "nianling" : 15 }
		{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "nianling" : 33 }
		{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 153 }
		{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 300 }
		{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 300, "date" : "2019-09-09" }
		{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123, "two" : "abs", "three" : null }
		>

		比较：
			$gt		大于
			$gte	大于等于
			$lt		小于
			$lte	小于等于
			$ne		不等于(not equee)
			
			例子：
				> db.xiyouji.find({age:{$gte:153}})
				{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 153 }
				{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 300 }
				{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 300, "date" : "2019-09-09" }
				> db.xiyouji.find({age:{$gt:153}})
				{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 300 }
				{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 300, "date" : "2019-09-09" }
				>
				> db.xiyouji.find({nianling:{$lt:33}})
				{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "nianling" : 15 }
				>
				> db.xiyouji.find({nianling:{$lte:33}})
				{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "nianling" : 15 }
				{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "nianling" : 33 }
				>
				> db.xiyouji.find({name:{$ne:'shasheng'}})
				{ "_id" : 123, "uer" : "123", "pw" : 234 }
				{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "nianling" : 15 }
				{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "nianling" : 33 }
				{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 153 }
				{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123, "two" : "abs", "three" : null }
				>
				> db.xiyouji.find({name:{$ne:'shasheng'}},{name:1})
				{ "_id" : 123 }
				{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji" }
				{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong" }
				{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie" }
				{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db") }

			
			
		关系：
			$and:[{}，{}]		同时满足条件
			$or:[{},{}]			满足一个条件即可
			
			例子：
				> db.xiyouji.find()
				{ "_id" : 123, "uer" : "123", "pw" : 234 }
				{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "nianling" : 15 }
				{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "nianling" : 33 }
				{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 153 }
				{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 300 }
				{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 300, "date" : "2019-09-09" }
				{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123, "two" : "abs", "three" : null }
				>
				> db.xiyouji.find({$and:[{name:'shasheng'},{"date" : "2019-09-09"}]})
				{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 300, "date" : "2019-09-09" }
				>
				> db.xiyouji.find({$or:[{age:153},{name:'wukong'}]})
				{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "nianling" : 33 }
				{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 153 }
				>
		
		
		存在性
			$exists:0	不存在
			$exists:1	存在
		
		例子：
			> db.xiyouji.find()
			{ "_id" : 123, "uer" : "123", "pw" : 234 }
			{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "nianling" : 15 }
			{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "nianling" : 33 }
			{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 153 }
			{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 300 }
			{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 300, "date" : "2019-09-09" }
			{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123, "two" : "abs", "three" : null }
			>
			> db.xiyouji.find({date:{$exists:1}})
			{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 300, "date" : "2019-09-09" }
			>
			> db.xiyouji.find({age:{$exists:0}})
			{ "_id" : 123, "uer" : "123", "pw" : 234 }
			{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "nianling" : 15 }
			{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "nianling" : 33 }
			{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123, "two" : "abs", "three" : null }
			>

		
		
		数据类型判断
		$type
			double	1
			string	2
			object	3
			array	4
			binary data	5
			object id	7
			boolean		10
			date	9
			null	10
			
			例子：
				> db.xiyouji.find()
				{ "_id" : 123, "uer" : "123", "pw" : 234, "dept" : "fomen" }
				{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "nianling" : 15, "dept" : "fomen" }
				{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "dept" : "fomen", "age" : "33years old" }
				{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 153, "dept" : "fomen" }
				{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 300, "dept" : "fomen" }
				{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 300, "date" : "2019-09-09", "dept" : "fomen" }
				{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123, "two" : "abs", "three" : null, "dept" : "fomen" }
				>
				> db.xiyouji.find({age:{$type:2}})
				{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "dept" : "fomen", "age" : "33years old" }
				>
				> db.xiyouji.find({age:{$type:1}})
				{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 153, "dept" : "fomen" }
				{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 300, "dept" : "fomen" }
				{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 300, "date" : "2019-09-09", "dept" : "fomen" }
				>

		
		
		
		
		
g.文档的修改
	db.集合.update({查询表达式},{新值},{选项})
	
	全部替换文档（相当于把匹配到的记录删除，重新写{新值}里面的内容）
		> db.xiyouji.find({_id:123})
		{ "_id" : 123, "name" : "adiwnfi", "key" : "erdfi234" }
		>
		> db.xiyouji.update({_id:123},{uer:'123',pw:123})
		WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
		>
		> db.xiyouji.find({_id:123})
		{ "_id" : 123, "uer" : "123", "pw" : 123 }

	
	修改指定文档（只修改指定属性的值）
	$set
		> db.xiyouji.update({_id:123},{$set:{pw:234}})
		WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
		> db.xiyouji.find({_id:123})
		{ "_id" : 123, "uer" : "123", "pw" : 234 }
		>

	
	删除某个属性
	$unset
		> db.xiyouji.find({one:123})
		{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123, "two" : "" }
		> db.xiyouji.update({one:123},{$unset:{two:""}})
		WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
		> db.xiyouji.find({one:123})
		{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123 }
		>

	
	重命名
	$rename:{旧属性名,新属性名}
		> db.xiyouji.find()
		{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123 }
		{ "_id" : 123, "uer" : "123", "pw" : 234 }
		{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "age" : 15 }
		{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "age" : 33 }
		{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 63 }
		{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 100 }
		{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 100, "date" : "2019-09-09" }
		>
		> db.xiyouji.update({name:'xiyouji'},{$rename:{'age':'nianling'}})
		WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
		> 
		> db.xiyouji.update({age:33},{$rename:{'age':'nianling'}})
		WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
		> 
		> db.xiyouji.find()
		{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123 }
		{ "_id" : 123, "uer" : "123", "pw" : 234 }
		{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "nianling" : 15 }
		{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "nianling" : 33 }
		{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 63 }
		{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 100 }
		{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 100, "date" : "2019-09-09" }
		
	
	
	列增长
	$inc
		> db.xiyouji.find({name:'bajie'})
		{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 63 }
		> db.xiyouji.update({name:'bajie'},{$inc:{age:-10}})
		WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
		> db.xiyouji.find({name:'bajie'})
		{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 53 }
		> db.xiyouji.update({age:53},{$inc:{age:100}})
		WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
		> db.xiyouji.find({name:'bajie'})
		{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 153 }


	修改多行数据
	{multi:true}
		注意：修改如果找到匹配的行，之修改1行，如果需要修改多行，使用multi选项
		> db.xiyouji.find()
		{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123 }
		{ "_id" : 123, "uer" : "123", "pw" : 234 }
		{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "nianling" : 15 }
		{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "nianling" : 33 }
		{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 153 }
		{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 100 }
		{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 100, "date" : "2019-09-09" }
		>
		> db.xiyouji.update({name:'shasheng'},{$set:{age:300}},{multi:true})
		WriteResult({ "nMatched" : 2, "nUpserted" : 0, "nModified" : 2 })
		>
		> db.xiyouji.find()
		{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123 }
		{ "_id" : 123, "uer" : "123", "pw" : 234 }
		{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "nianling" : 15 }
		{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "nianling" : 33 }
		{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 153 }
		{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 300 }
		{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 300, "date" : "2019-09-09" }
		>

		
	新增属性
	$set
		> db.xiyouji.find({one:123})
		{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123 }
		> 
		> db.xiyouji.update({one:123},{$set:{two:'abs',three:null}})
		WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
		> 
		> db.xiyouji.find({one:123})
		{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123, "two" : "abs", "three" : null }

		--给每一行都添加属性dept
		> db.xiyouji.update({},{$set:{dept:'fomen'}},{multi:true})
		WriteResult({ "nMatched" : 7, "nUpserted" : 0, "nModified" : 6 })
		>
		> db.xiyouji.find()
		{ "_id" : 123, "uer" : "123", "pw" : 234, "dept" : "fomen" }
		{ "_id" : ObjectId("5bfe313cf3bbac23bcd0d4f9"), "name" : "xiyouji", "nianling" : 15, "dept" : "fomen" }
		{ "_id" : ObjectId("5bfe3150f3bbac23bcd0d4fa"), "name" : "wukong", "nianling" : 33, "dept" : "fomen" }
		{ "_id" : ObjectId("5bfe315cf3bbac23bcd0d4fb"), "name" : "bajie", "age" : 153, "dept" : "fomen" }
		{ "_id" : ObjectId("5bfe3171f3bbac23bcd0d4fc"), "name" : "shasheng", "age" : 300, "dept" : "fomen" }
		{ "_id" : ObjectId("5bfe318af3bbac23bcd0d4fd"), "name" : "shasheng", "age" : 300, "date" : "2019-09-09", "dept" : "fomen" }
		{ "_id" : ObjectId("5bfe09c669ba2ff7f00750db"), "one" : 123, "two" : "abs", "three" : null, "dept" : "fomen" }
		>

		

练习
emp	集合
empno  员工号
hiredate 入职日期
ename   名字
sal         工资
comm   佣金
deptno 部门号

1.查询emp集合中工资大于2500的人的所有信息
db.emp.find({sal:{$gt:2500}})

3.查询emp集合中名字为ALLEN或者KING的人的工资和姓名、部门号
db.emp.find({$or:[{ename:'ALLEN'},{ename:"KING"}]},{sal:1,ename:1,deptno:1})

4.查询emp集合中部门为20号部门或者工资大于1500并且小于2500的人的所有信息
db.emp.find({$or:[{deptno:20},{$and:[{sal:{$gt:1500}},{sal:{$lt:2500}}]}]})

5.查询emp集合中名字为KING或者部门号为30号部门的人的姓名，佣金，部门号
db.emp.find({$or:[{ename:'KING'},{deptno:30}]},{ename:1,comm:1,deptno:1})

6.查询emp集合中雇佣号为7369的人的所有信息
db.emp.find({empno:7369})

7.查询emp集合中工资范围在800到1000的人或工资范围在2000到2500的人的所有信息
db.emp.find({$or:[
{$and:[{sal:{$gt:800}},{sal:{$lt:1000}}]},
{$and:[{sal:{$gt:2000}},{sal:{$lt:2500}}]}
]})

8.查询emp集合中工资高于1500，2000，2500的任何一个的人的所有信息
db.emp.find({$and:[{sal:{$gt:1500}},{sal:{$gt:2000}},{sal:{$gt:2500}}]})

9.查询emp集合中佣金不为空的人并且工资大于800，1500，2000的所有工资的人的所有信息
db.emp.find({$and:[{comm:{$exists:1}},{$and:[{sal:{$gt:800}},{sal:{$gt:1500}},{sal:{$gt:2000}}]}]})

db.emp.find({$and:[{comm:{$ne:null}},{$and:[{sal:{$gt:800}},{sal:{$gt:1500}},{sal:{$gt:2000}}]}]})

db.emp.find({$and:[{comm:{$type:{$ne:10}}},{$and:[{sal:{$gt:800}},{sal:{$gt:1500}},{sal:{$gt:2000}}]}]})

db.emp.find({$and:[{$or:[{comm:{$ne:null}},{comm:{$exists:1}}]},{$and:[{sal:{$gt:800}},{sal:{$gt:1500}},{sal:{$gt:2000}}]}]})
		






		