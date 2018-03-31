# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 16:26:32 2016

@author: hp
"""

import xlrd
import os
from xlrd import xldate_as_tuple
from datetime import datetime
import re

def get_items():
    file_dir=r'C:\cq\share_holding\raw'
    file_name=os.listdir(file_dir)
    file_path=[os.path.join(file_dir,fn) for fn in file_name]
    
    items=[]
    for fp in file_path:
        data=xlrd.open_workbook(fp)
        table=data.sheets()[0]
        nrows=table.nrows
        for r in range(1,nrows-2):
            line=table.row_values(r)
            sid=line[0]
            s=line[3]
            shares=re.findall(re.compile('\((\d+.*?)\)'),s)
            shares=[share.replace('SH','SS') for share in shares]
            d=line[4]
            date=datetime(*xldate_as_tuple(d,0)).strftime('%Y%m%d')
            items.append((sid,date,shares))
    return items

items=get_items()

stocks=[]
for item in items:
    if item[0] not in stocks:
        stocks.append(item[0])
    print item[0]

for stock in stocks:
    with open(r'C:\cq\share_holding\data\{stock}'.format(stock=stock.replace('SH','SS')),'w') as f:
        ticks=[]
        for item in items:
            if item[0]==stock:
                ticks.append(item)
                items.remove(item)
        ticks=sorted(ticks,key=lambda x:int(x[1]))
        for t in ticks:
            f.write(t[1]+'|'+'\t'.join(t[2])+'\n')
    print stock
        
