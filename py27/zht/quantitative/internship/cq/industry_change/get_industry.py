# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 13:33:19 2016

@author: Administrator
"""
from WindPy import *
from datetime import *
import pandas as pd
import time
w.start()


stocks=open(r'c:\industry_change\stocks.txt').read().split('\n')[:20]#######

tmp_data=w.wsd("600000.SH", "industry2", "2004-01-01", "2016-03-10", "industryType=1;industryStandard=1")######
#print data
industry=tmp_data.Data
dates=tmp_data.Times
#print industry[0][0].decode()
#print chardet.detect(industry[0][0])['encoding']



tmptime=time.time()
for industry_type in [1]:
    for industry_standard in [1]:
        data=w.wsd(','.join(stocks), "industry2","2016-01-01", "2016-03-10","industryType=%d;industryStandard=%d"%(industry_type,industry_standard))
        df=pd.DataFrame(data.Data,index=stocks)
        df.to_csv(r'c:\industry_change\%d_%d.csv'%(industry_type,industry_standard))
        print industry_type,industry_standard
