# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 13:33:19 2016

@author: Administrator
"""
from WindPy import *
from datetime import *
import time
w.start()


stocks=open(r'c:\industry_change\stocks.txt').read().split('\n')[:-1]#######

tmp_data=w.wsd("600000.SH", "industry2", "2004-01-01", "2016-01-6", "industryType=1;industryStandard=1")######
#print data
industry=tmp_data.Data
dates=tmp_data.Times
#print industry[0][0].decode()
#print chardet.detect(industry[0][0])['encoding']



tmptime=time.time()
for industry_type in [1,2,3,4]:
    for i in range(len(dates)):  
        f=open(r'c:\industry_change\data\%d\%s.txt'%(industry_type,str(dates[i].strftime('%Y%m%d'))),'w')
        data=[]
        for industry_standard in [1,2,3]:
            data.append(w.wsd(','.join(stocks), "industry2", "%s"%dates[i], "%s"%dates[i], "industryType=%d;industryStandard=%d"%(industry_type,industry_standard)))
        for m in range(len(stocks)):
            f.write('%s\t%s\t%s\t%s\n'%(stocks[m],data[0].Data[m][0].encode('gbk'),data[1].Data[m][0].encode('gbk'),data[2].Data[m][0].encode('gbk')))
#            if len(str(data[4][0]))!=0:
#                f.write('%s\t%s\t%s\t%s\t%s\n'%(stocks[m],data[0].Data[0][m][0],data[1].Data[m][0],data[2].Data[m][0],data[3].Data[m][0]))
#            else:
#                f.write('%s\t%s\t%s\t%s\n'%(stocks[m],data[0].Data[0][m][0],data[1].Data[m][0],data[2].Data[m][0]))
        print time.time()-tmptime,industry_type,dates[i]
        f.close()
        tmptime=time.time()

