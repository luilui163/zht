# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:33:19 2016

@author: Administrator
"""

import os
import pandas as pd



'''
注意，不同的行业industry1,2,3的split所用的字母不同
wind 是四级行业，其他的是三级行业
'''
path1=r'c:\GX'
path2=r'c:\industry_change\sw\changed'
files1=os.listdir(path1)
stocks=[f[:-4]for f in files1]
exchange_dates=open(r'c:\industry_change\dates.txt').read().split('\n')[:-1]
files2=os.listdir(path2)
changed_stocks=[f[:-4]for f in files2]

raw_lines=open(r'C:\industry_change\sw\20151231.txt').read().split('\n')[:-1]
stocks=[l.split('\t')[0] for l in raw_lines]
#industry1=[l.split('\t')[1].split('d')[1] for l in raw_lines]
#industry2=[l.split('\t')[2].split('d')[1] for l in raw_lines]
#industry3=[l.split('\t')[3].split('d')[1] for l in raw_lines]
#industry4=[l.split('\t')[4].split('d')[1] for l in raw_lines]
industrys=[l.split('\t')[1] for l in raw_lines]
#for m in range(len(industry1)):
#    dustry=(industry1[m]+'-'+industry2[m]+'-'+industry3[m]).decode('utf-8').encode('gb2312')
#    industrys.append(dustry)

for i in range(len(stocks)):
    if stocks[i] not in changed_stocks:
        path=os.path.join(path1,stocks[i]+'.txt')
        ipo_date=open(path).read().split('\n')[0].split('\t')[0]
        index=exchange_dates[exchange_dates.index(ipo_date):]
        df=pd.DataFrame([industrys[i]]*len(index),index=index,columns=[stocks[i]])
        df.to_csv(r'c:\industry_change\sw\unchanged\%s.csv'%stocks[i])
        print i
