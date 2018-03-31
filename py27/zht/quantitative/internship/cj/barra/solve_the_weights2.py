#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
import os

directory=r'C:\data\factors'
factor_names=os.listdir(directory)

date_intersection=[]
for i,fn in enumerate(factor_names):
    file_names=os.listdir(os.path.join(directory,fn))
    dates=[fn[:10] for fn in file_names]
    if i == 0:
        date_intersection=dates
    else:
        date_intersection=[d for d in date_intersection if d in dates]

date_union=[]
for fn in factor_names:
    file_names=os.listdir(os.path.join(directory,fn))
    dates=[fn[:10] for fn in file_names]
    for date in dates:
        if date not in date_union:
            date_union.append(date)
            date_union.sort()



for date in date_intersection:
    cross_df=pd.DataFrame()
    for factor_name in factor_names:
        path=os.path.join(directory,factor_name,date+'.csv')
        if os.path.isfile(path):
            tmp=pd.read_csv(path,index_col=0)
            cross_df=cross_df.append(tmp)
    cross_df.to_csv(r'C:\data\cross_sectional_data2\%s.csv' % date)
    print date






















