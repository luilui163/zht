# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:33:19 2016

@author: Administrator
"""
exchange_dates=open(r'C:\industry_change\exchange_dates.txt').read().split('\n')[:-1]

lines=open(r'C:\industry_change\sw\interval_new.txt').read().split('\n')[:-1]
stocks=[l.split('\t')[0] for l in lines]
start_dates=[l.split('\t')[1] for l in lines]
end_dates=[l.split('\t')[2] for l in lines]
f=open(r'C:\industry_change\sw\sw_extend.txt','w')
for i in range(len(stocks)):
    extend_start_date=[]
    extend_end_date=[]
    for j in range(len(exchange_dates)):
        if int(start_dates[i])<=int(exchange_dates[j]):
            extend_start_date=exchange_dates[j-5]
            break
    for k in range(j,len(exchange_dates)):
        if int(end_dates[i])<int(exchange_dates[k]):
            extend_end_date=exchange_dates[k]
            break
    f.write('%s\t%s\t%s\n'%(stocks[i],extend_start_date,extend_end_date))
    print i 
f.close()

