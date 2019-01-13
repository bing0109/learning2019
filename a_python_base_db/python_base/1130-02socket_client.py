#!usr/bin/env python
# _*_ coding:utf-8 _*_

import socket
ip_port = ('192.168.14.134', 51908)
sk = socket.socket()
sk.connect(ip_port)
sk.sendall(('i am client').encode())
ser_reply = sk.recv(1024)
print(ser_reply)
sk.close()

