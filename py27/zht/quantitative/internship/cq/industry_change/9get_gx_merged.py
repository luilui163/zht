# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:33:19 2016

@author: Administrator
"""

import os
import pandas as pd

path=r'c:\industry_change\sw\sw_raw'
files=os.listdir(path)
files_paths=[os.path.join(path,f) for f in files]
stocks=[]
for i in range(len(files_paths)):
    stock=files[i][:9]
#    print stock
    if stock not in stocks:
        f=open(r'c:\industry_change\sw\sw_merged\%s.txt'%stock,'w')
        f.write(open(files_paths[i]).read())
    else:
#        print stock
        f=open(r'c:\industry_change\\sw\sw_merged\%s.txt'%stock,'a')
        f.write(open(files_paths[i]).read())
    f.close()
    stocks.append(stock)
    print i



