#!/usr/bin/env python
'''
Created on 2017年3月25日

@author: admin
'''
#filecmp模块
#实践：检验源与备份目录差异
'''
dircmp类请看diff3.py记录
'''

import filecmp
import os
import re
import sys

from pip._vendor.distlib._backport import shutil


holderlist=[] 
def compareme(dir1,dir2):#递归获取更新项函数
    dircomp=filecmp.dircmp(dir1,dir2)
    #备份的文件包含两部分，一部分是源目录有的而目标目录没有的，一部分是源目录内更新过的
    only_in_one=dircomp.left_only #源目录新文件或目录,对比右边的文件，就是说只有左边有的，但右边没有的,备份的话左边源的话肯定是有最新的文件的
    diff_in_one=dircomp.diff_files#不匹配的文件，源目录的文件已发生变化
    dirpath=os.path.abspath(dir1)#定义源目录绝对路径
    #将更新的文件名或目录追加到holderlist
    ##os.path.join()把目录和文件名合成一个路径
    [holderlist.append(os.path.abspath(os.path.join(dir1,x))) for x in only_in_one]
    [holderlist.append(os.path.abspath(os.path.join(dir1,x))) for x in diff_in_one]
    if len(dircomp.common_dirs)>0:#判断是否存在相同子目录，以便递归
        for item in dircomp.common_dirs:#递归子目录
            print("递归开始")
            compareme(os.path.abspath(os.path.join(dir1,item)),os.path.abspath(os.path.join(dir2,item)))
    return holderlist
    
def main():
    if len(sys.argv)>2:
        dir1=sys.argv[1]
        dir2=sys.argv[2]
    else:
        print("Usage:",sys.argv[0],"datadir backupdir")#sys.argv[0]表示代码本身文件路径 python text1.py dir1 dir2
        sys.exit()
    source_files=compareme(dir1, dir2)#对比源目录与备份目录
    dir1=os.path.abspath(dir1)
    if not dir2.endswith('/'):dir2=dir2+'/'#备份目录加上"/"符
    dir2=os.path.abspath(dir2)
    destination_files=[]
    createdir_bool=False
    for item in source_files:#遍历返回的差异文件或目录清单
        destination_dir=re.sub(dir1,dir2,item)#将源目录差异路径清单对应替换成备份目录,就是在item目录或文件中将dir1换成dir2
        destination_files.append(destination_dir)
        if os.path.isdir(item):#如果差异路径为目录，并且在备份目录中不存在，则创建该目录
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
                createdir_bool=True#调用compareme函数标记
                
    if createdir_bool:#重新调用compareme函数，重新遍历新创建的目录内容，因上我们在dir2中又创建了一些新的目录
        destination_files=[]
        source_files=[]
        source_files=compareme(dir1,dir2)#调用compareme函数（重新来比较，因为在备份目录中新建 了一些与源目录相同的文件夹）
        for item in source_files:#获取源目录差异路径清单，对应替换成备份目录
            destination_dir=re.sub(dir1,dir2,item)
            destination_files.append(destination_dir)#确保了源目录与备份目录中的目录结构一致
    
    print("update item:")
    print(source_files)#输出更新列表
    #zip([seql, ...])接受一系列可迭代对象作为参数，将对象中对应的元素打包成一个个tuple（元组），然后返回由这些tuples组成的list（列表）。
    #若传入参数的长度不等，则返回list的长度和参数中长度最短的对象相同。
    '''
    zip函数
    x = [1, 2, 3]
    
    y = [4, 5, 6]
    
    z = [7, 8, 9]
    
    xyz = zip(x, y, z)
    
    print xyz
            复制代码
            运行的结果是：
    
    [(1, 4, 7), (2, 5, 8), (3, 6, 9)]
    '''
    copy_pair=zip(source_files,destination_files)#将源目录与备份目录文件清单拆分成元组，这两个列表数是相同的
    for item in copy_pair:
        if os.path.isfile(item[0]):#判断是否为文件，是则进行复制操作（因为上面的source_files与destination_files都是文件的最终路径，因为compareme有递归操作）
            shutil.copyfile(item[0], item[1])#item[0]代表的是源文件，item[1]为备份文件
           
            
if __name__=='__main__':    
            main()
