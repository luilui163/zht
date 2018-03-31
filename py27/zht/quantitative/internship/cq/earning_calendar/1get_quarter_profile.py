# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 13:48:20 2016

@author: Administrator
"""
import time 
import os
import pandas as pd


start=time.time()
path=r'C:\earning_calendar\reportdate'
files=os.listdir(path)
filesPath=[os.path.join('%s\%s'%(path,f)) for f in files]

date=[]
stock=[]
quarter=[]
for i in range(len(filesPath)):
    line=open(filesPath[i]).read().split('\n')[:-1]
    for j in range(len(line)):
        date.append(line[j].split(' ')[0])
        stock.append(line[j].split(' ')[1])
        quarter.append(line[j].split(' ')[2])

#change Q1 to 2004Q1
for m in range(len(quarter)):
    if quarter[m]=='Q1':
        for k in range(m-5,m+5):
            if len(quarter[k])==6 and quarter[k][-2:]=='Q1':
                quarter[m]=quarter[k]
#                print quarter[m]
                break
    if quarter[m]=='Q2':
        for k in range(m-5,m+5):
            if len(quarter[k])==6 and quarter[k][-2:]=='Q2':
                quarter[m]=quarter[k]
#                print quarter[m]
                break
    if quarter[m]=='Q3':
        for k in range(m-5,m+5):
            if len(quarter[k])==6 and quarter[k][-2:]=='Q3':
                quarter[m]=quarter[k]
#                print quarter[m]
                break
    if quarter[m]=='Q4':
        for k in range(m-5,m+5):
            if len(quarter[k])==6 and quarter[k][-2:]=='Q4':
                quarter[m]=quarter[k]
#                print quarter[m]
                break
    

category=sorted(list(set(quarter)))



for t in range(len(category)):
    f=open(r'c:\earning_calendar\quarter\%s.txt'%category[t],'w')
    for q in range(len(quarter)):
        if quarter[q]==category[t]:
            f.write('%s\t%s\n'%(date[q],stock[q]))
    f.close()


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    