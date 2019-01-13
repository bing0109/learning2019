#!usr/bin/env python
# _*_ coding:utf-8 _*_

import socket

ip_port = ('192.168.14.134', 51908)
sk = socket.socket()
sk.bind(ip_port)
sk.listen(5)

while True:
    print('welcom to honor!')
    conn, addr = sk.accept()
    client_data = conn.recv(1024)
    print(client_data)
    conn.sendall(('i am server,i have recevied your msg').encode())
    conn.close()
