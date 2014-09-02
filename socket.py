import socket


socket 连接
#                   IPv4              TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                   通信类型              协议家族   UDP为socket.SOCK_DGRAM

s.connect((‘ip地址’， port))



获取端口号  linux下  /etc/services

port = s.socket.getservbyname('http', 'tcp')    # host = socket.gethostbyname(hostname)
#                               端口名  为字符串      协议名  or 'udp'

s.getsockname()  #本机的ip和port 
s.getpeername()  #远程机器的ip和port



socket 通信                                        sendto('发送数据', (host, port))    recvfrom(2048)[0] # recvfrom返回元组（接收数据，发送数据的地址）

socket对象                              s.send()    sendto()     recv()     recvfrom()
#    关闭连接 s.shutdowm()  s.close()
文件对象   fd = s.makefile('rw', 0)     fd.write()               read()                 readline()
#                                缓存，关闭为0   如果用缓存，结束必须调用fd.flush()
#   UDP 不用文件对象


UDP 通信
data = sys.stdin.readline().strip()
s.sendall(data)     # 发送数据包



Network Servers

服务器连接过程
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #    1，建立socket对象
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #  2，设置socket选项（可选）
S.s.bind((host, port))                                  #   3，绑定到一个端口（同样，也可以是一个指定的网卡）
s.listen(5)                                            #    4，侦听连接

s.setsockopt(level, optname, value)
level: socket选项，
optname：选项的参数
        SOL_SOCKET常用到的选项参数  SO_BINDTODEVICE, SO_BROADCAST, SO_DONTROUTE, SO_KEEPALIVE, SO_OOBINLINE, SO_REUSEADDR, SO_TYPE
value: 参数的值

s.getsockopt(level, optname [, buflen])
                            # 指定buflen 返回字符串     不指定返回整数


