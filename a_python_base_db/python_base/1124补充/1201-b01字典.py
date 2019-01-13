学习目标
掌握字段的日常操作


课程内容
a.字段的应用场景
b.创建字段
c.访问字段
d.修改字段
e.删除字段
f.补充





a.字段的应用场景
    1.前后端数据传输
    2.浏览器提交数据给服务器
    3.接口开发


b.创建字段
    字段是python中的映射类型，由键值组成   name:"value"
    一般用数字或字符串作为键
    dic = {'name':'feiyang','age':28}


c.访问字段
    >>> dic = {'name':'feiyang','age':28}
    >>>
    >>> dic
    {'age': 28, 'name': 'feiyang'}
    >>> print(dic)
    {'age': 28, 'name': 'feiyang'}
    >>>


d.修改字典
    >>> dic={'name':'heygor','QQ':110}
    >>> print(dic)
    {'QQ': 110, 'name': 'heygor'}
    >>> dic['qq'] = '232'
    >>> print(dic)
    {'QQ': 110, 'qq': '232', 'name': 'heygor'}
    >>>




e.删除字段
    1.del
        删除元素
        >>> del dic['age']
        >>> print(dic)
        {'name': 'feiyang'}
        >>>
        删除整个字典
        >>> del dic
        >>> print(dic)
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        NameError: name 'dic' is not defined
        
    2.clear    
        清空字典
        >>> dic={'name':'heygor','QQ':110}
        >>>
        >>> print(dic)
        {'QQ': 110, 'name': 'heygor'}
        >>> dic.clear()
        >>> print(dic)
        {}
        
       
f.补充
    1.keys（键）
        >>> print(dic)
        {'QQ': 110, 'qq': '232', 'name': 'heygor'}
        >>> print(dic.keys())
        ['QQ', 'qq', 'name']
        >>> for i in dic.keys():
        ...     print i
        ...
        QQ
        qq
        name

    2.values(值)   
        >>> print(dic.values())
        [110, '232', 'heygor']
        >>> for i in dic.values():
        ...     print i
        ...
        110
        232
        heygor
        >>>

    3.items（键和值）
        >>> print(dic.items())
        [('QQ', 110), ('qq', '232'), ('name', 'heygor')]
        >>>
        >>> for i in dic.items():
        ...     print(i)
        ...
        ('QQ', 110)
        ('qq', '232')
        ('name', 'heygor')
        >>>
        >>> for i,j in dic.items():
        ...     print(i,j)
        ...
        ('QQ', 110)
        ('qq', '232')
        ('name', 'heygor')
        >>>




练习
1.设计一个登陆的程序，不同的用户名和对应密码存在一个字典里面，输入正确的用户名和密码去登陆，
2.首先输入用户名，如果用户名不存在或者为空，则一直提示输入正确的用户名
3.当用户名正确的时候，提示去输入密码，如果密码跟用户名不对应，则提示密码错误请重新输入。         

us_pw = {'abc':'123','dev':'456'}

while True:
    user = input('please input user name:')
    if us_pw.count(user) != 1:
        print('please input the right user name!')
        continue
    else:
        pw = input('please input password:')
        if us_pw[user] == None:
            print('please input password!')
        
        elif us_pw[user] != pw:
            print('username and pw not match, please input again!')
            break
        
        elif us_pw[user] == pw:
            print('congratuations,username match the pw!')


    









