'''
部署LNMP业务环境
通过env.roledefs定义不同主机角色，再使用@roles('webservers')修饰符绑定到对应的任务函数
实现不同角色主机的部署差异

本例子通过角色来区别不同业务服务环境，分别部署不同的程序包，
'''
#!/usr/bin/env python
from fabric.colors import *
from fabric.api import *

env.user='root'
env.roledefs = {#定义角色分组
    'webservers': ['192.168.1.21', '192.168.1.22'],
    'dbservers': ['192.168.1.23']
}

env.passwords = {
    'root@192.168.1.21:22': 'SKJh935yft#',
    'root@192.168.1.22:22': 'SKJh935yft#',
    'root@192.168.1.23:22': 'KJSD9325hgs'
}

@roles('webservers')#webtask任务函数'引用webservers'角色修饰符
def webtask():#部署nginx php php-fpm等环境
    print yellow("Install nginx php php-fpm...")
    with settings(warn_only=True):
        run("yum -y install nginx")
        run("yum -y install php-fpm php-mysql php-mbstring php-xml php-mcrypt php-gd")
        run("chkconfig --levels 235 php-fpm on")
        run("chkconfig --levels 235 nginx on")

@roles('dbservers')#datask任务函数引用'dbservers'角色修饰符
def dbtask():#部署mysql
    print yellow("Install Mysql...")
    with settings(warn_only=True):
        run("yum -y install mysql mysql-server")
        run("chkconfig --levels 235 mysqld on")

@roles ('webservers', 'dbservers')#publictask函数同时引用两个角色修饰符
def publictask():
    print yellow("Install epel ntp...")
    with settings(warn_only=True):
        run("rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm")
        run("yum -y install ntp")

def deploy():#部署公共类环境，如epel,ntp等
    execute(publictask)
    execute(webtask)
    execute(dbtask)
'''

'''
