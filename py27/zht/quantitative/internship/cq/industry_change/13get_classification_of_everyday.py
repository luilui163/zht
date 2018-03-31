# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:33:19 2016

@author: Administrator
"""

import os
import pandas as pd
import chardet


df=pd.read_csv(r'C:\industry_change\sw\sw.csv',index_col=0)
for i in range(len(df)):
    dates=[d for d in df.index]
    tmp=df.iloc[i]
    tmp=tmp.dropna()
#    for m in range(len(tmp)):
#        if chardet.detect(tmp.values[m])['encoding']=='utf-8':
#            tmp.values[m]=tmp.values[m].decode('utf-8').encode('gb2312')
            
    f=open(r'C:\industry_change\sw\sw_txt\%s.txt'%dates[i],'w')
    for k in range(len(tmp)):
        if tmp.values[k]!='---':
            f.write('%s\t%s\n'%(tmp.index[k],tmp.values[k]))
    f.close()
    print i
    
    