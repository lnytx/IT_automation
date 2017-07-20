'''
文件打包，上传与校验
'''
#!/usr/bin/env python
from _threading_local import local
from cProfile import run
from nt import abort
from test.test_threaded_import import task

from django.conf import settings
from pip._vendor.requests.api import put

from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm


env.user='root'
env.hosts=['192.168.1.21','192.168.1.22','192.168.1.23']
env.password='SKJh935yft#'


@task
@runs_once
def tar_task():#本地打包函数，只执行一次
    with lcd("/data/logs"):
        local("tar -czf access.tar.gz access.log")
@task
def put_task():#上传文件任务函数
    run("mkdir -p /data/logs")
    with cd("/data/logs"):
        with settings(warn_only=True):
            result = put("/data/logs/access.tar.gz", "/data/logs/access.tar.gz")#put（上传）出现异常时继续执行，非终止
        if result.failed and not confirm("put file failed, Continue[Y/N]?"):
            abort("Aborting file put task!")#出现异常时，确认用户是否继续

@task
def check_task():#校验文件任务函数
    with settings(warn_only=True):
        #本地local命令需要配置capture=True才能捕获返回值
        lmd5=local("md5sum /data/logs/access.tar.gz",capture=True).split(' ')[0]
        rmd5=run("md5sum /data/logs/access.tar.gz").split(' ')[0]
    if lmd5==rmd5:#对比本地及远程的md5信息
        print "OK"
    else:
        print "ERROR"

@task
def go():
    tar_task()
    put_task()
    check_task()
