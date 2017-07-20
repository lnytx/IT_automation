'''
Created on 2017年3月25日

@author: admin
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
print('\n'.join(diff1))
d2=difflib.HtmlDiff()
print("diff2",d2.make_file(test1_lines, test2_lines))

    
        
        
        
        
        
        
        
        
        


