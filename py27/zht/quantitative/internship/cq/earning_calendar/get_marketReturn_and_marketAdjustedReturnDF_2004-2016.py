# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 19:51:55 2016

@author: Administrator
"""
import pandas as pd

returnDF=pd.read_csv(r'c:\returnDF_2004-2016.csv',index_col=0)


returnDF1=returnDF[returnDF<0.11]
returnDF2=returnDF1[returnDF1>-0.11]
#mean 使用的是有效数据，忽略了nan，个数也是除去了nan的个数
test1=list(returnDF2.mean(axis=1))# change the series to list for the convenience of the writing in the below
date=[d for d in returnDF.index]
f=open(r'c:\marketReturn_2004-2016.txt','w')


for i in range(len(test1)):
    f.write('%d\t%f\n'%(date[i],test1[i]))
f.close()


marketAdjustedReturnDF=returnDF2
for m in range(len(returnDF2)):
    for n in range(len(returnDF2.T)):
        marketAdjustedReturnDF.iat[m,n]=returnDF2.iat[m,n]-test1[m]
print m
marketAdjustedReturnDF.to_csv(r'c:\marketAdjustedReturnDF_2004-2016.csv')

'''
#最简洁的方式
df=pd.read_csv(r'c:\marketAdjustedReturnDF_2004-2016.csv',index_col=0)
df[df>0.11]=np.nan
df[df<-0.11]=np.nan

df.apply(lambda x:x-df.mean(axis=1))
'''