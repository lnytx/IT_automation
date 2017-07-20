'''
Created on 2017年3月26日

@author: admin

双向同步文件操作
远程文件自动打包并下载
通过使用spawn()方法执行ssh,scp命令来实现
'''

import sys

from django.contrib.sessions.backends import file
import pexpect
from pexpect.exceptions import EOF, TIMEOUT


ip="192.168.1.21"
user="root"
passwd="H6DSY#*$df32"
target_file="/data/logs/nginx_access.log"

child = pexpect.spawn('/usr/bin/ssh', [user+'@'+ip])
fout = file('mylog.txt','w')
child.logfile = fout

try:
    child.expect('(?i)password')
    child.sendline(passwd)
    child.expect('#')
    child.sendline('tar -czf /data/nginx_access.tar.gz '+target_file)
    child.expect('#')
    print (child.before)
    child.sendline('exit')
    fout.close()
except EOF:
    print ("expect EOF")
except TIMEOUT:
    print ("expect TIMEOUT")

#启动scp远程复制命令，实现将打包好的文件复制到本地/home目录
child = pexpect.spawn('/usr/bin/scp', [user+'@'+ip+':/data/nginx_access.tar.gz','/home'])
fout = file('mylog.txt','a')
child.logfile = fout
try:
    child.expect('(?i)password')
    child.sendline(passwd)
    child.expect(pexpect.EOF)#匹配缓存冲区EOF（结尾），保证复制正常完成
except EOF:
    print ("expect EOF")
except TIMEOUT:
    print ("expect TIMEOUT")
