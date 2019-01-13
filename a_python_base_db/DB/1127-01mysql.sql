1、笛卡尔积
	当查询数据时，一张表无法满足查询条件，使用多表查询
	两张表不做任何关联产生的数据
	
	表1
	1
	2
	
	表2
	1 a
	2 b
	3 c
	
	表1、表2的笛卡尔积如下
	1 1 a
	1 2 b
	1 3 c
	2 1 a
	2 2 b
	2 3 c
	
	
	如下，笛卡尔积灰导致数量成倍增加，无效数据增多，降低系统性能	
	mysql> select count(*) from city;
	+----------+
	| count(*) |
	+----------+
	|      600 |
	+----------+
	1 row in set (0.06 sec)
	
	mysql> select count(*) from country;
	+----------+
	| count(*) |
	+----------+
	|      109 |
	+----------+
	1 row in set (0.09 sec)
	
	mysql> select count(*) from city,country;
	+----------+
	| count(*) |
	+----------+
	|    65400 |
	+----------+
	1 row in set (0.10 sec)
	
	为避免产生笛卡尔积，使用内联查询、左联查询、右联查询
	
	内联查询：
		语法：
			select 列 from 表1 inner join 表2 on 表1.列 = 表2.列;
			select 列 from 表1,表2 where 表1.列=表2.列;
			
		例子：
			select * from city,country where city.country_id = country.country_id and country.country = 'China';
			
			select co.country from city c,country co where c.country_id = co.country_id and c.city = 'Daxian'; 
			c co是表别名
	
		练习：
			查询国家名称为China的并且城市名称以D开头的所有城市名称
			select c.city from city c,country co where c.country_id = co.country_id and co.country = 'China' and c.city like 'D%';
			
			查询客户名字为Mike所在的国家名称
		select co.country from customer cu,address ad,city c, country co
		where cu.address_id = ad.address_id
		and ad.city_id = c.city_id
		and c.country_id = co.country_id
		and cu.first_name = 'MIKE';



	
	
	
	图片1练习
	3.1
		select * from Test1,Test2 
		where Test1.No = Test2.No
		and Test1.Department = "计算机系"
		and Test1.Place = "北京";
		
		select * from Test1 where Department = "计算机系" and Place = "北京";
	
	3.2
		update Test1 set Department = "信息学院" where Department = "计算机系";
	
	3.3
		select t1.No,t1.Name,t2.Grade,t2.Courses from Test1 t1,Test2 t2
		where t1.No = t2.No
		and t2.Grade >= 75;
	
	
	图片4练习
	1.A
		select S.S#,SC.GRADE from S,SC where S.S# = SC.S# AND SC.C# = 'C2';
		select S#,Grade from SC where C# = 'C2';
		
	1.B
		SELECT SNAME FROM S WHERE SNAME LIKE 'D%';
	
	1.C
		SELECT S.S#,S.SNAME FROM S,SC,C
		WHERE S.S# = SC.S#
		AND SC.C# = C.C#
		AND C.CNAME = 'Maths';
		
	1.D
		SELECT S# FROM SC WHERE C# IN ('C2','C4');
		
		
		
		
		
		
		
		
		
		
2、子查询
	一条SQL语句的查询依赖于另一条SQL语句的执行结果
	
	例子：
		查询国家名称为China的城市名称有哪些？
			select city from city where country_id = (select country_id from country where country='China');
		查询country表中最大country_id的国家名称
			select country from country where country_id = (select max(country_id) from country);
		
	注意：
		子查询可以用于在数据查询、新增、修改、删除方面
		
	补充：
		查询子句查询处理的结果可能是一个也可能是多个，如果是多个的话，不能用=，用in
		单行子查询	=
		多行子查询	in
		
		
	练习：
		1.用子查询查询国家名称为China的所有D开头的城市名称
		select city from city 
		where country_id=(select country_id from country where country = 'China') 
		and city like 'D%';
		
		2.用子查询查询城市名称为Daxian的所有客户的姓名
		(x)select first_name from customer
		where address_id = (select address_id from address where city_id = (select city_id from city where city = 'Daxian'));
		
		select first_name from customer
		where address_id in (select address_id from address where city_id in (select city_id from city where city = 'Daxian'));
	
	
	
	作业：
	标准SQL嵌套语句，指子查询
	图7
		1.
		SELECT S.S#,S.SN FROM S,SC
		WHERE S.S#=SC.S#
		AND SC.C#=(SELECT C# from C WHERE CN = '税收基础');
		
		select s#,SN from S where s# in (select s# from sc where c# in (SELECT C# from C WHERE CN = '税收基础'));
		
		2.
		SELECT S.SN,S.SD FROM S,SC
		WHERE S.S#=SC.S#
		AND SC.C#= 'C2';
		
		select sn,sd from s where s# in (select s# from c# where c# = 'C2');
		
		
		3.
		SELECT S.SN,S.SD FROM S,SC
		WHERE S.S#=SC.S#
		AND SC.C# IS NOT 'C5';
		
		select sn,sd from s where s# in (select s# from c# where c# is not 'C5');
		
		4.
		SELECT COUNT(SSC.S#) FROM (SELECT S.S# FROM S,SC WHERE S.S#=SC.S# GROUP BY S.S#) SSC;
		
		5.
		SELECT S.S#,S.SD FROM S
		WHERE S.S# in (
		SELECT SSC.S# FROM (SELECT S.S#,COUNT(S.S#) FROM S,SC WHERE S.S#=SC.S# GROUP BY S.S#) SSC WHERE SSC.COUNT(S.S#)>5
		);
		
		SELECT S.S#,S.SD FROM S
		WHERE S.S# in (SELECT S.S# FROM S,SC WHERE S.S#=SC.S# GROUP BY S.S# HAVING COUNT(S.S#)>5);
		
	
	
	
	
	
	
	
分组查询
	a.分组函数（聚合）
		max()
		min()
		avg()
		sum()
		count()
		
		分组函数通常和分组一起使用，也可以单独使用
		
		例子：
			select max(city_id),min(city_id) from city;
		
		
	b.分组
		按照某种条件进行分类
		语法：
			select 列 from 表
			where 条件
			group by 分组条件
			having 分组后过滤条件
			
		分组条件的判断：
			每后面跟的需求就是分组条件
			
		例子：
			select country_id,count(city) from city
			group by country_id;
	
			
			select co.country,count(*) from city c,country co
			where c.country_id=co.country_id
			group by co.country;
			
	
		分组后过滤
			where 	分组前过滤	不能直接跟分组函数
			having	分组后过滤	可以直接跟分组函数
	
			例子：查询城市数量大于50的国家名称
			select co.country from city c,country co
			where c.country_id=co.country_id
			group by co.country
			having count(*) >50;
			
		
		补充：
			分组分为单分组和多分组，安装分组条件进行分类
			eg.每个门店 每天 的营业总额？
				group by 门店，天
	
	
	
	
	作业：
	图3
		1.
		select * from dt_Pay
		where salary > (select avg(salary) from dt_Pay);
		
		2.
		select de.emploryid,de.emploryname,dp.job,dp.salary,dp.bonus from dt_Emp de,dt_Pay dp
		where de.emploryid = dp.emploryid;
		
		select * from dt_Pay;
	
		3.
		(x)truncate dt_Pay;
		truncate table dt_Pay;(用delete删除，自增长字段不能初始化)
	
	图6
		这是oracle相关的题目，varchar2是oracle里面的字段，比varchar存储多一倍的长度
		1.
		create table USER(
		USERID int primary key comment '用户ID',
		USERNAME varchar(20) not null comment '用户名',
		PASSWORD varchar(20) not null comment '密码',
		CRTIME date not null comment '创建时间'
		);
		
		create table USER(
		USERID int primary key,
		USERNAME varchar2(20) not null,
		PASSWORD varchar2(20) not null,
		CRTIME date not null comment
		);

		
		2.
		(mysql)insert into USER values(1002,'username','password','2015-01-01');
		(oracle)insert into USER values(1002,'username','password',to_date('2015-01-01','YYYY-MM-DD'));
	
	
		3.用熟悉的一种语言打印出九九乘法口诀表
	
	
	
	图 qq笔试
		1.
		select * from emp where deptno = '30';
		
		2.
		select emp.ename, emp.empno, dept.dname from emp, dept 
		where emp.deptno = dept.deptno
		and emp.empno = (select empno from emp where job = '办事员');

		3.
		select ename from emp where comm > sal;

		4.
		select ename from emp where comm > (sal*1.6);

