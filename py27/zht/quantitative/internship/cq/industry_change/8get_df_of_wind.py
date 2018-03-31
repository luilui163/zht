# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:33:19 2016

@author: Administrator
"""

import os
import pandas as pd



df=pd.read_csv(r'c:\industry_change\wind.csv',index_col=0)

dates=open(r'C:\industry_change\dates.txt').read().split('\n')[:-1]
lines=open(r'D:\class\WIND\WIND_20160101.txt').read().split('\n')[:-1]
stocks=[l.split('\t')[0] for l in lines]
industrys=[]
for i in range(len(lines)):
    industry1=lines[i].split('\t')[1].split('d')[1]
    industry2=lines[i].split('\t')[2].split('d')[1]
    industry3=lines[i].split('\t')[3].split('d')[1]
    tmp='-'.join([industry1,industry2,industry3])
    industrys.append(tmp)


df_stocks=[s for s in df.columns]
for j in range(len(stocks)):
    if stocks[j] not in df_stocks:
        tmp_df=pd.DataFrame([industrys[j].decode('utf-8').encode('gb2312')]*len(dates),index=[int(d) for d in dates],columns=[stocks[j]])
        df=pd.concat([df,tmp_df],axis=1)
        print j,stocks[j]

df=df.fillna(method='ffill')
df=df.fillna(method='bfill')

#df.to_csv(r'c:\industry_change\wind_new.csv')

'''
str.decode('gb2312').encode('utf-8')
'''


for i in range(len(df)):
    f=open(r'C:\industry_change\wind_industry\%s.txt'%df.index[i],'w')
    for j in range(len(df.T)):
        f.write('%s\t%s\n'%(df.columns[j][:9],df.iat[i,j]))
f.close()
'''
problem1:
 






