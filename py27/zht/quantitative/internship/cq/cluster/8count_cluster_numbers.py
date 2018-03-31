# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:43:49 2016

@author: Administrator
"""
import os 
from pyExcelerator import *

path=r'C:\cluster\hcluster\second'

file_name=os.listdir(path)
file_path=[os.path.join(path,f) for f in file_name]
w=Workbook()
ws=w.add_sheet(path.split('\\')[-1])
for i in range(len(file_path)):
    line=open(file_path[i]).read().split('\n')[:-1]
    stock=[l.split('\t')[0] for l in line]
    industry=[l.split('\t')[1] for l in line]
    
    category=list(set(industry))
    count=[0]*len(category)
    for s in range(len(industry)):
        count[category.index(industry[s])]+=1
    count=sorted(count,reverse=True)
    ws.write(0,i,file_name[i][:-4])
    for m in range(len(count)):
        ws.write(m+1,i,count[m])
w.save(r'C:\cluster\number\20160331\%s.xls'%path.split('\\')[-1])
    

