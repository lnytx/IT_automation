'''
Created on 2017年3月25日

@author: admin
'''
#filecmp模块
'''
cmp:单文件对比 
filecmp.cmp(f1,f2[,shallow])方法
shallow默认为True，根据os.stat()方法返回文件的，比如最后的访问时间，修改时间，状态改变时间等，
不会对比文件的内容

cmpfiles:多文件对比（应该是有比对文件内容的）
filecmp.cmpfiles(dir1,dir2,common[,shallow])
这个方法是目录为参数，对比dir1,dir2两个目录给定的文件清单，返回文件名的三个列表，
分别是1、匹配，匹配是包含匹配的文件的列表，2、不匹配，3、错误，错误是指包括了目录不存的文件
或者是不具备读取权限或其他原因导致的不能比较的文件
eg:filecmp.cmpfiles("/dir1","/dir2",['f1','f2','f3','f4','f5'])
输出{['f1','f2'],['f3'],['f4','f5']]}
上面输出表示f1,与f2匹配，f3不匹配，f4,f5匹配，

dircmp:目录对比
通过dircmp(a,b[,ignore][,hide])类创建一个对象,a,b为目录名,ignore忽略的列表
默认为['RCS','CVS','tags'],hide参数代表隐藏的列表，默认为[os.curdir,os.pardir]
dircmp类可以获取目录比较的详细信息，如只在a中存在的文件、a与b中都存在的文件
dircmp提供了三个输出报告的方法
report(),比较当前指定目录中的内容：
report_partial_closure(),比较当前指定目录及第一级子目录中的内容
report_full_closure(),递归比较所有指定目录的内容

dircmp类还提供了以下的属性
left_list：左边文件夹中的文件与文件夹列表； 
•right_list：右边文件夹中的文件与文件夹列表； 
•common：两边文件夹中都存在的文件或文件夹； 
•left_only：只在左边文件夹中存在的文件或文件夹； （对比右边的文件，就是说只有左边有的，但右边没有的）
•right_only：只在右边文件夹中存在的文件或文件夹； 
•common_dirs：两边文件夹都存在的子文件夹； 
•common_files：两边文件夹都存在的子文件； 
•common_funny：两边文件夹都存在的子文件夹； 
•same_files：匹配的文件； 
•diff_files：不匹配的文件； 
•funny_files：两边文件夹中都存在，但无法比较的文件； 
•subdirs：我没看明白这个属性的意思，python手册中的解释如下：A dictionary mapping names in common_dirs to dircmp objects 

'''
import filecmp
a="/dir1"
b="/dir2"
dirobj=filecmp.dircmp(a,b,['text.py'])#目录比较，忽略test.py文件
#输出对比结果报表
dirobj.report()
dirobj.report_partial_closure()
dirobj.report_full_closure()
print("left_list",str(dirobj.left_list))


