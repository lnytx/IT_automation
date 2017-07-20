'''
Created on 2017年3月26日

@author: admin
'''
'''
scapy一个强大的交互式数据所处理程序，能对数据进行伪造或解包，包括发送数据包，包嗅探，应答和反馈等
可以用来处理网络扫描，路由跟踪，服务探测，单元测试等

本实践是通过traceroute()方法实现路由的跟踪，跟踪动态结果动态生成图形格式
'''
# -*- coding: utf-8 -*-

import os, sys, time, subprocess
import warnings, logging

from pip._vendor.distlib.compat import raw_input

from scapy.all import traceroute


warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
domains = raw_input('Please input one or more IP/domain: ')
target =  domains.split(' ')
dport = [80]
if len(target) >= 1 and target[0]!='':
    res,unans = traceroute(target,dport=dport,retry=-2)
    res.graph(target="> test.svg")
    time.sleep(1)
    subprocess.Popen("/usr/bin/convert test.svg test.png", shell=True)
else:
    print ("IP/domain number of errors,exit")
