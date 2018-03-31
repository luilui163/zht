# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 14:35:15 2016

@author: Administrator
"""
import os
from WindPy import *
from datetime import *
import pandas as pd
import time
w.start()

def update_classification(folder,date):
    for m in ['sw','wind','zx','gx']:
        if not os.path.isdir(os.path.join(folder,m)):
            os.makedirs(os.path.join(folder,m))
    classification={1:'sw',2:'wind',3:'zx',4:'gx'}
    for industryType in [1,2,3,4]:
#        date=time.strftime("%Y%m%d",time.localtime(time.time()))

        stocks=w.wset("sectorconstituent","date=%s;sectorid=a001010100000000"%date).Data[1]
        industrys=w.wsd(stocks, "industry2", date, date, "industryType=%d;industryStandard=5"%industryType).Data[0]
        if len(industrys)!=1:
            f=open(folder+'\%s\%s.txt'%(classification[industryType],date),'w')
            for i in range(len(stocks)):
                f.write('%s\t%s\n'%(stocks[i].encode('gb2312'),industrys[i].encode('gb2312')))
            f.close()
        else:
            break

if __name__=='__main__':
#    update_classification(r'c:\garbage\update_classification')

#    dates=open(r'c:\anaconda\zht\date1.txt').read().split('\n')[:-1]
#    dates=b[:24]
    dates.reverse()
    for date in dates:
        update_classification(r'c:\garbage\update_classification',date)
        print date

'''
获得date的方法
import tushare as ts
a=ts.get_hist_data('000016')
index=list(a.index)
dates=[i.replace('-','') for i in index]
'''


