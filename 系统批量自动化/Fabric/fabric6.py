'''
程序发布要求具备源代码打包，发布，切换，回滚，版本管理等功能
本实例就实现了这一整套流程的功能
其中版本回滚使用了linux下的软链接实现

'''

#!/usr/bin/env python
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
import time

env.user='root'
env.hosts=['192.168.1.21','192.168.1.22']
env.password='SKJh935yft#'

env.project_dev_source = '/data/dev/Lwebadmin/'#开发机项目主目录
env.project_tar_source = '/data/dev/releases/'#开发机项目压缩包存储目录
env.project_pack_name = 'release'#项目压缩包名前缀，文件名为rewlease.tar.gz

env.deploy_project_root = '/data/www/Lwebadmin/'#项目生产环境主目录
env.deploy_release_dir = 'releases' #项目发布目录，位于主目录下面
env.deploy_current_dir = 'current'#对外服务的当前版本软链接

env.deploy_version=time.strftime("%Y%m%d")+"v2"#版本号

@runs_once
def input_versionid():#获得用户输入的版本号，以便做版本回滚操作
    return prompt("please input project rollback version ID:",default="")

@task
@runs_once
def tar_source():#打包本地项目主目录，并将压缩包存储到本地压缩包目录
    print yellow("Creating source package...")
    with lcd(env.project_dev_source):
        local("tar -czf %s.tar.gz ." % (env.project_tar_source + env.project_pack_name))
    print green("Creating source package success!")


@task
def put_package():#上传任务函数
    print yellow("Start put package...")
    with settings(warn_only=True):
        with cd(env.deploy_project_root+env.deploy_release_dir):
            run("mkdir %s" % (env.deploy_version))#创建 版本目录
    env.deploy_full_path=env.deploy_project_root + env.deploy_release_dir + "/"+env.deploy_version

    with settings(warn_only=True):#上传项目压缩包到此目录
        result = put(env.project_tar_source + env.project_pack_name +".tar.gz",env.deploy_full_path)
    if result.failed and no("put file failed, Continue[Y/N]?"):
        abort("Aborting file put task!")

    with cd(env.deploy_full_path):#成功解压后删除压缩包
        run("tar -zxvf %s.tar.gz" % (env.project_pack_name))
        run("rm -rf %s.tar.gz" % (env.project_pack_name))

    print green("Put & untar package success!")


@task
def make_symlink():#为当前版本目录做软链接
    print yellow("update current symlink")
    env.deploy_full_path=env.deploy_project_root + env.deploy_release_dir + "/"+env.deploy_version
    with settings(warn_only=True):#删除 软链接，重新创建并指定软链接源目录，新版本生效
        run("rm -rf %s" % (env.deploy_project_root + env.deploy_current_dir))
        run("ln -s %s %s" % (env.deploy_full_path, env.deploy_project_root + env.deploy_current_dir))
    print green("make symlink success!")

@task
def rollback():#版本回滚函数
    print yellow("rollback project version")
    versionid= input_versionid()
    if versionid=='':
        abort("Project version ID error,abort!")

    env.deploy_full_path=env.deploy_project_root + env.deploy_release_dir + "/"+versionid
    run("rm -f %s" % env.deploy_project_root + env.deploy_current_dir)
    #删除 软链接，重新创建并指定软链接源目录，新版本生效
    run("ln -s %s %s" % (env.deploy_full_path, env.deploy_project_root + env.deploy_current_dir)) 
    print green("rollback success!")

@task
def go():#自动化程序 版本发布入口函数
    tar_source()
    put_package()
    make_symlink()
