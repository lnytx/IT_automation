'''
Created on 2017年3月26日

@author: admin


Fabric基于Python2.5及以上版本实现 的ssh命令行工具，简化了SSH的应用程序部署及系统管理任务，
它提供了系统基础的操作组件，可以实现本地或远程shell命令，包括命令执行，文件上传，下载及完整执行日志传输
Fabric在paramiko的基础上做了更高一层的封装，操作起来更为简单

本示例调用local()方法执行本地命令，添加@runs_once修饰符保证该任务了函数只执行一次，调用run()方法执行远程命令
'''

#!/usr/bin/env python
from _threading_local import local
from cProfile import run

from fabric.api import *


env.user='root'
env.hosts=['192.168.1.21','192.168.1.22']
env.password='SKJh935yft#'

@runs_once
def local_task():
    local("uname -a")

def remote_task():
    with cd("/data/logs"):#with 的作用是让后面的表达式的语句继承当前状态，实现cd /data/logs && ls -l的效果
        run("ls -l")
