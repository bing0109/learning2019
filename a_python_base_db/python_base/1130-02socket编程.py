# coding=utf-8
# author = cjb

学习目标
    掌握socket编程基本方法


内容
    a.socket定义
    b.socket对象
    c.socket编程思路
    d.开发实例


a.socket定义
    即套接字，用于描述IP、端口等，通过链路句柄，应用程序通过套接字向网络中发出请求或应答
    socket遵循“一切皆为文件”思想，可以打开，读取，关闭
    
    socket和file区别：
        file模块是针对指定文件打开、读写、关闭
        socket模块是指针对服务器和客户端socket进行打开、读写、关闭
        
    


b.socket对象

    sk = socket.socket(socket.AT_INET, socket.socket_stream, 0)
        参数1：地址簇（IPV4，IPV6）
        参数2：协议（tcp/udp）


c.socket编程思路
    
    c1.tcp服务端
        1.创建套接字，绑定套接字到本地IP和端口
        2.开始监听连接
        3.进入循环，不断接受客户端连接请求
        4.接受传来的数据，并且发送数据给对方
        5.传输完毕，关闭套接字
        
    c2.tcp客户端
        1.创建套接字，连接远程地址
        2.连接后发送数据和接收数据
        3.传输完毕，关闭套接字


d.开发实例
    1.server.py
    #encoding=utf-8
    import socket
    #以元组形式定义一个ip和port
    ip_port=('127.0.0.1',9999)
    #创建对象并进行绑定IP和进行监听
    sk =  socket.socket()
    #绑定地址到套接字
    sk.bind(ip_port)
    #开始监听传入连接（可以挂起的最大连接数）
    sk.listen(5)
    
    while True:
        print('welcom!')
        #conn代表客户端和服务端建立连接的通信链路
        conn,addr = sk.accept()
        #accept表示阻塞方式，没收到连接请求就不会向下执行
        
        #从client接受的消息
        client_data = conn.recv(1024)
        print(client_data)
        
        #回复消息
        conn.sendall(('server reviced your message').encode())

        #关闭连接
        sk.close()




    1.client.py
    #encoding=utf-8
    import socket
    #需要连接的服务器ip和地址
    ip_port=('127.0.0.1',9999)
    创建对象并进行绑定IP和进行监听
    sk.socket.socket()
    #连接address套接字
    sk.connect(ip_port)
    
    #向服务器发送数据
    sk.sendall(('im client!').encode())
    
    #接收服务器的数据并打印出来
    ser_reply = sk.recv(1024)
    print(ser_reply)
    
    关闭连接
    sk.close()





