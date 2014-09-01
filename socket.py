import socket


socket 连接
#                   IPv4              TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                   通信类型              协议家族   UDP为socket.SOCK_DGRAM

s.connect（（‘ip地址’， port））

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
