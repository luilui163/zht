# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:33:19 2016

@author: Administrator
"""

from WindPy import *
from datetime import *
import pandas as pd
import time
w.start()

lines=open(r'c:\industry_change\sw\sw_extend.txt').read().split('\n')[:-1]
for i in range(len(lines)):
    stock=lines[i].split('\t')[0]
    start_date=lines[i].split('\t')[1]
    end_date=lines[i].split('\t')[2]
    data=w.wsd(stock,"industry2",start_date,end_date,"industryType=1;industryStandard=5")
    f=open(r'c:\industry_change\sw\sw_raw\%s_%f.txt'%(stock,time.time()),'w')
    for j in range(len(data.Times)):
        f.write('%s\t%s\n'%(str(data.Times[j].strftime('%Y%m%d')),data.Data[0][j].encode('gbk')))
    f.close()
#
#    str(dates[i].strftime('%Y%m%d'))











 