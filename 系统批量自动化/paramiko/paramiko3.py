'''
Created on 2017年3月26日

@author: admin

利用paramiko的invoke_shell机制来实现通过保磊机实现服务器操作
原理是SSHClient.connect到堡垒机后开启一个新的ssh会话,
通过新的会话运行"ssh user@IP"去实理远程执行命令的操作
'''

#!/usr/bin/env python
import paramiko
import os,sys,time

hostname="192.168.1.21" #定义业务服务器信息
username="root"
password="SKJh935yft#"

blip="192.168.1.23"#堡垒机信息
bluser="root"
blpasswd="SKJh935yft#"

port=22
passinfo='\'s password: '#输入服务器密码的前标志串
paramiko.util.log_to_file('syslogin.log')

#登录堡垒机
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=blip,username=bluser,password=blpasswd)

#new session
channel=ssh.invoke_shell()#创建新会话，开启命令调用
channel.settimeout(10)#会话命令执行超时时间，单位为秒

buff = ''
resp = ''
channel.send('ssh '+username+'@'+hostname+'\n')#执行ssh登录业务主机

while not buff.endswith(passinfo):#ssh登录的提示信息判断，输出尾串含有"\'s password:"时退出循环
    try:
        resp = channel.recv(9999)
    except Exception as e:
        print ('Error info:%s connection time.' % (str(e)))
        channel.close()
        ssh.close()
        sys.exit()
    buff += resp
    if not buff.find('yes/no')==-1:#输出串含有"yes/no"时发送“yes”并回画
        channel.send('yes\n')
    buff=''

channel.send(password+'\n')#发送业务主机密码

buff=''
while not buff.endswith('# '):#输出串为“#”时说明校验通过并退出循环
    resp = channel.recv(9999)
    if not resp.find(passinfo)==-1:#输出中尾含有"\'s password:"时，说明密码不正确，要求重新输入
        print ('Error info: Authentication failed.')
        channel.close()#关闭连接对象后退出
        ssh.close()
        sys.exit() 
    buff += resp

channel.send('ifconfig\n')#认证通过后发送ifconfig命令来查看结果
buff=''
try: 
    while buff.find('# ')==-1:
        resp = channel.recv(9999)
        buff += resp
except Exception as e:
    print ("error info:"+str(e))

print (buff)
channel.close()
ssh.close()
