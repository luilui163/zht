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


#date='20160627'
##a=w.wset("sectorconstituent","date=%s;sectorid=a001010100000000"%'20160627')
#stocks=w.wset("sectorconstituent","date=%s;sectorid=a001010100000000"%date).Data[1]
#
#data=w.wss("000001.SZ,000004.SZ", "concept","tradeDate=20160630").Data[0]

content=open(r'c:\cq\stock.txt').read().split('\n')[:-1]
stocks=[]
for c in content:
    if c[-1]=='Z':
        stocks.append(c)
    else:
        stocks.append(c[:-1]+'H')

path=r'c:\cq\date.txt'
dates=open(path).read().split('\n')[:500][::-1]
for date in dates:
#    stocks=w.wset("sectorconstituent","date=%s;sectorid=a001010100000000"%date).Data[1]
    concept=w.wss(stocks,'concept','tradeDate=%s'%date).Data[0]

    f=open(r'c:\cq\concept\wind\%s.txt'%date,'w')
    for i in range(len(concept)):
        if concept[i]!=None:
            f.write('%s\t%s\n'%(stocks[i].encode('utf-8'),concept[i].encode('gbk')))
    f.close()
    print date



