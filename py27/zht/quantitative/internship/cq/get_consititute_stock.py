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

#dates=open(r'c:\garbage\new_date.txt').read().split('\n')[:-1]
dd=open(r'c:\garbage\dd.txt').read().split('\n')

dd=['20160515']
#for d in dd:
#    f=open(r'C:\cq\ZZ500\%s.txt'%d,'w')
#    stocks=w.wset("sectorconstituent","date=%s;windcode=000905.SH"%d).Data[1]
#    f.write('\n'.join(stocks))
#    f.close()
#    print d

#ZZ500 000905.SH
#HS300 000300.SH

for d in dd:
    
    data=w.wset("indexconstituent","date=%s;windcode=000300.SH"%d)
    weights=data.Data[3]
    stocks=data.Data[1]
    stocks=map(lambda x:x.replace('SH','SS'),stocks)
    
    t=['\t']*len(stocks)
    z=zip(stocks,t,[str(we) for we in weights])
    
    f=open(r'c:\cq\HS300\%s.txt'%d,'w')
    f.write('\n'.join(map(lambda a:a[0]+a[1]+a[2],z)))
    f.close()
    print d


#def sh2ss(x):
#    x=x.replace('SH','SS')
#    return x
#new_stocks=map(sh2ss,stocks)



