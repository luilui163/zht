# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 13:33:19 2016

@author: Administrator
"""
from WindPy import *
from datetime import *
import time
w.start()


stocks=open(r'c:\industry_change\stocks.txt').read().split('\n')[:]#######

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
        for j in range(len(stocks)):
            industry=[]
            for industry_standard in [1,2,3,4]:
                data=w.wsd("%s"%stocks[j], "industry2", "%s"%dates[i], "%s"%dates[i], "industryType=%d;industryStandard=%d"%(industry_type,industry_standard))
                if data.Data[0][0]!=None:
                    industry.append(data.Data[0][0].encode('gbk'))
            if len(industry)==4:
                f.write('%s\t%s\t%s\t%s\t%s\n'%(stocks[j],industry[0],industry[1],industry[2],industry[3]))
            if len(industry)==3:
                f.write('%s\t%s\t%s\t%s\n'%(stocks[j],industry[0],industry[1],industry[2]))
        print time.time()-tmptime,industry_type,dates[i]
        f.close()
        tmptime=time.time()
######打印到txt的是乱码，怎么解决
