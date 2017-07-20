'''
Created on 2017年3月26日

@author: admin
'''
'''
1、安装clamav这款免费并开源的防毒软件
2、pyClamad是python第三方模块，可让Python直接使用ClamAV病毒扫描守护进程 clamd，来实现一个高效的冱检测功能
3、更新守护进程监听IP配置文件，根据不同的环境自行修改监听的IP，’0.0.0.0‘为监听所有主机IP
sed -i -e '/^TCPAddr/{ s/127/0/0/1/0.0.0.0/; }' /etc/clamd.conf
4、安装pyClamad模块

本实例通过Clamdnetwork.Socket()方法实现与业务服务器建立扫描连接，再通过启动不同的扫描方式实施病毒扫描，并返回结果
也就是相当于从服务器通过 连接去扫描坡业务服务器
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
import time

import pyclamd


class Scan(Thread):

    def __init__ (self,IP,scan_type,file):
        """构造方法"""
        Thread.__init__(self)
        self.IP = IP
        self.scan_type=scan_type
        self.file = file
        self.connstr=""
        self.scanresult=""


    def run(self):
        """多进程run方法"""

        try:
            cd = pyclamd.ClamdNetworkSocket(self.IP,3310)#创建网络套接字连接对象
            if cd.ping():
                self.connstr=self.IP+" connection [OK]"
                cd.reload()#重载clamd病毒特征库，建议更新病毒库后做reload()操作
                if self.scan_type=="contscan_file":
                    self.scanresult="{0}\n".format(cd.contscan_file(self.file))
                elif self.scan_type=="multiscan_file":
                    self.scanresult="{0}\n".format(cd.multiscan_file(self.file))
                elif self.scan_type=="scan_file":#选择不同的扫描方式
                    self.scanresult="{0}\n".format(cd.scan_file(self.file))
                time.sleep(1)
            else:
                self.connstr=self.IP+" ping error,exit"
                return
        except Exception as e:
            self.connstr=self.IP+" "+str(e)


IPs=['127.0.0.1','192.168.1.22']#扫描的主机列表 
scantype="multiscan_file"#存储扫描Scan类线程对象列表
scanfile="/data/www"
i=1
threadnum=2
scanlist = []

for ip in IPs:

    currp = Scan(ip,scantype,scanfile)#创建Scan类对象，参数（IP，扫描模式,扫描路径）
    scanlist.append(currp)#追加对象到列表

    if i%threadnum==0 or i==len(IPs):#当达到指定的线程数或IP列表数后启动、退出线程
        for task in scanlist:
            task.start()

        for task in scanlist:
            task.join()#等待所有子线程退出，并输出扫描结果
            print (task.connstr)#打印服务器连接信息
            print (task.scanresult)#打印扫描结果
        scanlist = []   
    i+=1