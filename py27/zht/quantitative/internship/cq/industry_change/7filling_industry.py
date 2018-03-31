# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:33:19 2016

@author: Administrator
"""
import os
import pandas as pd

path=r'C:\industry_change\zx_new'
files=os.listdir(path)
files_paths=[os.path.join(path,f) for f in files]
files_paths=sorted(files_paths)
stocks=[f[:9] for f in files]
dates=open(r'c:\industry_change\dates.txt').read().split('\n')[:-1]

k=0
lines=open(files_paths[k]).read().split('\n')[:-1]
dates=[l.split('\t')[0] for l in lines]
industrys=[l.split('\t')[1] for l in lines]
stock_name=files_paths[k].split('_')[2][-9:]
#df=pd.DataFrame(industrys,index=dates,columns=[stock_name])
lines=open(r'C:\GX\%s.txt'%stock_name).read().split('\n')[:-1]
exchange_dates=[l.split('t')[0] for l in lines]
df=pd.DataFrame(industrys,index=dates,columns=[stock_name])

#for m in range(1,len(files_paths)):
#    tmp_lines=open(files_paths[m]).read().split('\n')[:-1]
#    tmp_dates=[l.split('\t')[0] for l in tmp_lines]
#    tmp_industrys=[l.split('\t')[1] for l in tmp_lines]
#    tmp_df=pd.DataFrame(tmp_industrys,index=tmp_dates,columns=[files_paths[m].split('_')[2][-9:]])
#    df=pd.concat([df,tmp_df],axis=1)
#    print m
#
#
#df=df.fillna(method='ffill')
#df=df.fillna(method='bfill')
#df.to_csv('c:\industry_change\zx.csv')



