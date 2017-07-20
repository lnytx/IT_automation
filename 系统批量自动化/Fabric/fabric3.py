'''
本示例通过fabric的env对象定义中转机（堡垒机）
再结合任务函数实现目标主机文件上传与执行的操作

通过配置env.gateway='192.168.0.1'就可以轻松实现堡垒机环境的文件上传及执行，相比paramiko的实现方法简洁了很多，
编写的任务函数完全不用考虑堡垒机的环境
配置env.gateway即可
'''
#!/usr/bin/env python
from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm

env.user='root'
env.gateway='192.168.1.23'#定义堡垒机，作为文件上传，执行的中转设备
env.hosts=['192.168.1.21','192.168.1.22']
#假如所有的主机密码都不一样，可以通过env.passwords字典变量一一指定
env.passwords = {
    'root@192.168.1.21:22': 'SKJh935yft#',
    'root@192.168.1.22:22': 'SKJh935yft#',
    'root@192.168.1.23:22': 'KJSD9325hgs'#堡垒机账号信息
}

lpackpath="/home/install/lnmp0.9.tar.gz"#本地安装包路径
rpackpath="/tmp/install"#远程安装包路径

@task
def put_task():
    run("mkdir -p /tmp/install")
    with settings(warn_only=True):
        result = put(lpackpath, rpackpath)#上传安装包
    if result.failed and not confirm("put file failed, Continue[Y/N]?"):
        abort("Aborting file put task!")

@task
def run_task():#执行远程命令，安装lnmp环境
    with cd("/tmp/install"):
        run("tar -zxvf lnmp0.9.tar.gz")
        with cd("lnmp0.9/"):
            run("./centos.sh")

@task
def go():
    put_task()
    run_task()
