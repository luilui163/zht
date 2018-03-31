# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:33:19 2016

@author: Administrator
"""
import os
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

start=time.time()

return_df=pd.read_csv(r'c:\bloomberg_new\return_df1.csv',index_col=0)
for i in range(len(return_df.T)):
    tmp_df=return_df.iloc[:,i]
    date=int(tmp_df.name)
    lines=open(r'C:\industry_change\daily\zx\%d.txt'%date).read().split('\n')[:-1]
    stocks=[l.split('\t')[0] for l in lines]
    zx1=[l.split('\t')[1].split('-')[0] for l in lines]
    zx2=[l.split('\t')[1].split('-')[1] for l in lines]
    zx3=[l.split('\t')[1].split('-')[2] for l in lines]
    zx_df=pd.DataFrame({'zx1':zx1,
                        'zx2':zx2,
                        'zx3':zx3},index=stocks)
                        
    lines=open(r'C:\industry_change\daily\gx\%d.txt'%date).read().split('\n')[:-1]
    stocks=[l.split('\t')[0] for l in lines]
    gx1=[l.split('\t')[1].split('-')[0] for l in lines]
    gx2=[l.split('\t')[1].split('-')[1] for l in lines]
    gx3=[l.split('\t')[1].split('-')[2] for l in lines]
    gx_df=pd.DataFrame({'gx1':gx1,
                        'gx2':gx2,
                        'gx3':gx3},index=stocks)
    
    
    lines=open(r'C:\industry_change\daily\sw\%d.txt'%date).read().split('\n')[:-1]
    stocks=[l.split('\t')[0] for l in lines]
    sw1=[l.split('\t')[1].split('-')[0] for l in lines]
    sw2=[l.split('\t')[1].split('-')[1] for l in lines]
    sw3=[l.split('\t')[1].split('-')[2] for l in lines]
    sw_df=pd.DataFrame({'sw1':sw1,
                        'sw2':sw2,
                        'sw3':sw3},index=stocks)
    
    
    lines=open(r'C:\industry_change\daily\wind\%d.txt'%date).read().split('\n')[:-1]
    stocks=[l.split('\t')[0] for l in lines]
    wind1=[l.split('\t')[1].split('-')[0] for l in lines]
    wind2=[l.split('\t')[1].split('-')[1] for l in lines]
    wind3=[l.split('\t')[1].split('-')[2] for l in lines]
    wind4=[l.split('\t')[1].split('-')[3] for l in lines]
    wind_df=pd.DataFrame({'wind1':wind1,
                        'wind2':wind2,
                        'wind3':wind3,
                        'wind4':wind4},index=stocks)
                        
                        
    target_df=pd.concat([tmp_df,zx_df,gx_df,sw_df,wind_df],axis=1)
    target_df=target_df.dropna()
    col=[c for c in target_df.columns]
    col[0]='returns'
    target_df.columns=col
    target_df.to_csv(r'c:\bloomberg_new\df_of_everyday\%d.csv'%date)
    print i






