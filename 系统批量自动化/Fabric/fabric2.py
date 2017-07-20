'''
本示例使用@task修饰符标志入口函数go()对外部可见
配合"@runs_once"修饰符接收用户输入
最后调用worktask()任务函数，实现远程命令执行
'''

#!/usr/bin/env python
from cProfile import run
from smtplib import prompt
from test.test_threaded_import import task

from fabric.api import * 


env.user='root'
env.hosts=['192.168.1.21','192.168.1.22']
env.password="SKJh935yft#"

'''
该示例实现了一个动态输入远程目录名称，再获取目录列表的功能，由于我们只要求输入一次，再显示所有主机上该目录的列表信息
，调用了一个子函数input_raw()同时配置@runs_once修饰符来达到此目的
'''

@runs_once#主机遍历中，只有第一台触发此函数
def input_raw():
    return prompt("please input directory name:",default="/home")

def worktask(dirname):
    run("ls -l "+dirname)

@task#限定只有go函数对fab命令可见
def go():
    getdirname = input_raw()
    worktask(getdirname)
