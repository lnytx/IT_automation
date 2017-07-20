'''
Created on 2017年3月26日

@author: admin

paramiko是基于python实现 的ssh2远程安全连接，支持认证及密钥方式，可以实现远程命令执行，文件传输，中间ssh代理功能，
相对于pexpect，paramiko封装得更高，更贴近ssh协议功能
核心组件为
SSHClient类：是ssh服务会话的高级表示 ，封装了传输，通道，及SFTPClient的校验，建立的方法，通常用于执行远程命令
SFTPClient类：作为一个SFTP客户端对象，根据SSH传输协议的sftp会话，实现远程文件操作，比如文件上传，下载，权限，状态等操作
'''

#!/usr/bin/env python
import paramiko


hostname='192.168.1.21'
username='root'
password='SKJh935yft#'
paramiko.util.log_to_file('syslogin.log')#  送paramiko日志到syslogin.log文件

ssh=paramiko.SSHClient()#创建一个ssh客户端client对象
ssh.load_system_host_keys()#获取客户端host_keys，默认~/.ssh/known_hosts,非默认路径需要指定
ssh.connect(hostname=hostname,username=username,password=password)#创建ssh连接
stdin,stdout,stderr=ssh.exec_command('free -m')#调用远程执行命令方法exec_command()
print (stdout.read())#打印命令执行结果，得到Python列表形式，可以使用stdout,readlines()
ssh.close()#关闭ssh连接
