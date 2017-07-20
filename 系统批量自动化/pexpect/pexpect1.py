'''
Created on 2017年3月26日

@author: admin

pexpect是Python的一个普通模块，可以实现对ssh,ftp,passwd,telnet等命令进行自动交互，而无需人工干涉到达到
自动化的目的
包括spawn，run函数，及派生类pxssh
'''
'''
spawn类：
spawn是pexpect的主要类接口，功能是启动和控制子程序应用程序，
child=pexpect.spawn('/usr/bin/ftp')启动ftp客户端命令
child=pexpect.spawn('ls  -latr /tmp')
当子程序需要参数时，还可以使用Python列表来代替参数项
child=pexpect('ls', ['-latr','/tmp'])
下面是一个完整的示例，实现了一个ssh连接远程主机并执行命令的示例
首先使用login()方法与远程主机建立连接，再通过sendline()方法发送执行的命令
prompt()方法等待命令执行结束且出现系统提示符，最后使用logout()方法断开 连接
'''

from cmath import e
import getpass

import pexpect
from pip._vendor.distlib.compat import raw_input
import pxssh


try:
    s = pxssh.pxssh()#创建pxssh对象s
    hostname = raw_input('hostname: ')
    username = raw_input('username: ')
    password = getpass.getpass('password: ')#接收密码输入
    s.login (hostname, username, password)#建立ssh连接
    s.sendline ('uptime')  # run a command
    s.prompt()             # match the prompt匹配系统提示符
    print (s.before)         # print everything before the prompt.
    s.sendline ('ls -l')
    s.prompt()
    print (s.before)
    s.sendline ('df')
    s.prompt()
    print (s.before)
    s.logout()
except pxssh.ExceptionPxssh as e:
    print ("pxssh failed on login.")
    print (str(e))

