# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 13:39:16 2016

@author: hp
"""

def change_date(date):
    month,day,year=tuple(date.split(r'/'))
    if len(month)==1:
        month='0'+month
    if len(day)==1:
        day='0'+day
    return year+month+day


lines=open(r'C:\cq\investor_research\data\data1.txt').read().split('\n')[:-1]
with open(r'c:\cq\investor_research\data\data.txt','w') as f:
    for l in lines:
        stock=l.split('\t')[0].replace('SH','SS')
        number=l.split('\t')[1]
        date=change_date(l.split('\t')[2])
        industry1=l.split('\t')[3]
        industry2=l.split('\t')[4]
        f.write('\t'.join([date,stock,number,industry1,industry2])+'\n')