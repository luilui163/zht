# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:33:19 2016

@author: Administrator
"""

import os

path=r'd:\class\GX'
files=os.listdir(path)
files_paths=[os.path.join(path,f) for f in files]
files_paths=sorted(files_paths,key=lambda x:int(x[-12:-4]))


def get_snapshot(number,files_paths):
    p=number
    lines=open(files_paths[p]).read().split('\n')[:-1]
    stocks=[0]*len(lines)
    first=[0]*len(lines)
    second=[0]*len(lines)
    third=[0]*len(lines)
    for i in range(len(lines)):
        stocks[i]=lines[i].split('\t')[0]
        first[i]=lines[i].split('\t')[1]
        second[i]=lines[i].split('\t')[2]
        third[i]=lines[i].split('\t')[3]
#        fourth[i]=lines[i].split('\t')[4]
    return (stocks,first,second,third)


f=open(r'c:\industry_change\gx.txt','w')
#target_stocks=[]
#target_dates1=[]
#target_dates2=[]
for k in range(1,len(files_paths)):
    (stocks0,first0,second0,third0)=get_snapshot(k-1,files_paths)
    (stocks1,first1,second1,third1)=get_snapshot(k,files_paths)

    for i in range(len(stocks0)):
        if stocks0[i] in stocks1:
            if third0[i]!=third1[stocks1.index(stocks0[i])]:
                f.write('%s\t%s\t%s\n'%(stocks0[i],files_paths[k-1][-12:-4],files_paths[k][-12:-4]))
#                target_stocks.append(stocks0[i])
#                target_dates1.append(files_paths[k-1][-12:-4])
#                target_dates2.append(files_paths[k][-12:-4])
f.close()


