'''
Created on 2017年3月26日

@author: admin
本例子使用pexpect模块的spawnu()方法执行FTP命令，通过expect()方法定义匹配的输出规则，
sendlin()方法执行相关的FTP交互命令等
'''
from __future__ import unicode_literals

import pexpect
import sys

child = pexpect.spawnu('ftp ftp.openbsd.org')
child.expect('(?i)name .*: ')
child.sendline('anonymous')
child.expect('(?i)password')
child.sendline('pexpect@sourceforge.net')
child.expect('ftp> ')
child.sendline('bin')
child.expect('ftp> ')
child.sendline('get robots.txt')
child.expect('ftp> ')
sys.stdout.write (child.before)
print("Escape character is '^]'.\n")
sys.stdout.write (child.after)
sys.stdout.flush()
child.interact() # Escape character defaults to ^]
child.sendline('bye')
child.close()
