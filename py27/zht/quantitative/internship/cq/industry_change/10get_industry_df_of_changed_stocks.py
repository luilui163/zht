# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:33:19 2016

@author: Administrator
"""

import os
import pandas as pd

path1=r'c:\GX'
path2=r'C:\industry_change\sw\sw_merged'
exchange_dates=open(r'c:\industry_change\dates.txt').read().split('\n')[:-1]
files=os.listdir(path2)
files_paths=[os.path.join(path2,f) for f in files]



for i in range(len(files_paths)):
    lines=open(files_paths[i]).read().split('\n')[:-1]
    dates=[l.split('\t')[0] for l in lines]
    industrys=[l.split('\t')[1] for l in lines]
#    df=pd.DataFrame(industrys,index=dates,columns=[files_paths[i][-13:-4]])    
    
    stock_name=files[i]
    ipo_date=open(os.path.join(path1,stock_name)).read().split('\n')[0].split('\t')[0]
    index=exchange_dates[exchange_dates.index(ipo_date):]
    zero=[None]*len(index)
    for k in range(len(industrys)):
        if dates[k] in index:
            zero[index.index(dates[k])]=industrys[k]
    df=pd.DataFrame(zero,index=index,columns=[stock_name[:-4]])
    df=df.fillna(method='ffill')
    df=df.fillna(method='bfill')
    df.to_csv(r'C:\industry_change\sw\changed\%s.csv'%stock_name[:-4])
    print i,stock_name








