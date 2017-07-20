#-*-coding:utf-8 -*-
'''
Created on 2017年3月25日

@author: admin
'''
#diff的第二个上例子，读取两个文件的不一致
#文件读取分隔函数
import sys
import difflib


def readfile(filename):
    try:
        #with open("myfile.txt") as f:
        fileHandle=open(filename,'rb')
        text=fileHandle.read().test_splitlines()#以行进行分离
        fileHandle.close()
        return text
    except IOError as error:
        print("Read file Error"+str(error))

#定义两个文件
textfile1=''
textfile2=''
if textfile1=="" or textfile2=="":
    print("Usage:diff2.py filename1 filename2")#linux下当成脚本执行
    sys.exit()
text1_lines=readfile(textfile1)
text2_lines=readfile(textfile2)
d=difflib.HtmlDiff()
print(d.make_file(text1_lines,text2_lines))#输出html格式


