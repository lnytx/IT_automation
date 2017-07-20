#coding:utf-8
'''
Created on 2017年3月25日

@author: admin
'''
#psutil
'''
psuti能够轻松获取系统运行的进程和系统利用率（包括CPU，内存，磁盘，网络等）
主要用于系统监控，分析和限制系统资源及进程的管理实现了同等命令行工具如
ps,top,lsof,netsat,ifconfig,who,df,kill,free,nice,ionice,iostat
等命令
'''
#IPy模块
'''
包含IP类，可以处理大部分格式为IPv6和IPv4的网络地址
1、IP个数，及所有的IP地址清单
2、反射解析名称，IP类型，IP转换，子网数
'''
#dnspython
'''
用于所有记录类型，用于查询，传输并动态更新ZONE信息，同时支持事物签名，验证消息和扩展DNS
可以利用其查询功能来实现DNS服务监控以及解析结果的校验，可以代替nslookup及dig工具
'''
#difflib(python自带模块)
'''
实现两个字符串的差异对比
  11a
+ asdfas45
+ dfsg
+ retw
- adsfasdgadsffgasdfasd2re3terydfg
- aa
- dd
输出符号含义
-:包含在第一个序列行中，但不包含在第二个序列行中
+:包含在第二个序列行中，但不包含在第一个序列行中
'':空白的则表示是两序列行一致
'?':标志两个序列行存在增量差异
'^':标志两个序列行存在的差异字符

'''
import difflib
text1="""
11a
adsfasdgadsffgasdfasd2re3terydfg
aa
dd
67
67
"""
text2='''
11a
asdfas45
dfsg
retw
'''
test1_lines=text1.splitlines()#按行分割
test2_lines=text2.splitlines()
d1=difflib.Differ()#创建Differ对象
diff1=d1.compare(test1_lines, test2_lines)#使用compare方法对比字符串
print('diff1\n'.join(diff1))
d2=difflib.HtmlDiff()
print("diff2",d2.make_file(test1_lines, test2_lines))
#diff的第二个上例子，读取两个文件的不一致


