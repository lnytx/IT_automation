'''
Created on 2017年3月26日

@author: admin
'''
x = [1, 2, 3]
y = [4, 5, 6]
z = [7, 8, 9]
xyz = zip(x, y, z)
    
for item in xyz:
    print(item[0],item[1])