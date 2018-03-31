# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 15:37:49 2016

@author: hp
"""

import os
folder_path=r'C:\cq\basicratio_quartely'

file_names=os.listdir(folder_path)
file_path=[os.path.join(folder_path,fn) for fn in file_names if '2' in fn]


lines=open(r'C:\cq\basicratio_quartely\colsname.txt').read().split('\n')
for l in lines:
    items=l.split('"')
    for i in range(len(items)):
        print i,items[i]

title=[items[4*i-1] for i in range(2,33)]

with open(r'C:\cq\basicratio_quartely\data.txt','w') as f:
    f.write('stock\tdate\tannouncementdate\t%s\n'%('\t'.join(title)))
    f.write('sid\tdate\tannouncementdate\tdate%s\n'%('\tc'*31))
    for fp in file_path:
        lines=open(fp).read().split('\n')[:-1]
        date=fp[-12:-4]
        for l in lines:
            items=l.split('"')
            stock=items[0][:-1]
            data=[items[4*i-1].replace(',','') for i in range(1,33)]
            f.write('%s\t%s\t%s\n'%(stock,date,'\t'.join(data)))
        print fp

lines=open(r'c:\cq\announcement\raw_data.txt').read().split('\n')[:-1]
with open(r'c:\cq\announcement\data.txt','w') as f:
    for l in lines:
        items=l.split('\t')
        del items[2]
        f.write('%s\n'%('\t'.join(items)))
        
        
        
        
        