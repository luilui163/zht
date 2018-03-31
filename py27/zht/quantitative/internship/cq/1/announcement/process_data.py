# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 11:27:41 2016

@author: hp
"""

import os
import pandas as pd
import numpy as np
import csv


def shift_date(d,shift_num=1):
    d=int(d)
    if shift_num>0:
        if d<return_df_dates[0]:
            print d,'out of return_df_date\'s range'
        elif d>return_df_dates[-shift_num-1]:
            return return_df_dates[-1]
        elif d in return_df_dates:
            ind=return_df_dates.index(d)
            return return_df_dates[ind+shift_num]
        else:
            for i in range(len(return_df_dates)):
                if return_df_dates[i]<d and return_df_dates[i+1]>d:
                    return return_df_dates[i+shift_num]
    elif shift_num==0:
        if d<return_df_dates[0]:
            print d,'is too small'
        elif d>return_df_dates[-1]:
            print d,'is too large'
        elif d in return_df_dates:
            return d
        else:
            for i in range(len(return_df_dates)):
                if return_df_dates[i]<d<return_df_dates[i+1]:
                    return return_df_dates[i+1]
    elif shift_num<0:
        num=-shift_num
        if d<return_df_dates[num-1]:
            print d,'is too small'
        elif d>return_df_dates[-1]:
            print d,'is too large'
        elif d in return_df_dates:
            ind=return_df_dates.index(d)
            return return_df_dates[ind-num]
        else:
            for i in range(len(return_df_dates)):
#                if return_df_dates[i]<=d and return_df_dates[i+1]>d:
                if return_df_dates[i]<d<return_df_dates[i+1]:
                    return return_df_dates[i+1-num]
                    
return_df=pd.read_csv(R'c:\cq\return_df.csv',index_col=0)
return_df_dates=list(return_df.index)
return_df_stocks=list(return_df.columns)





file_dir=r'C:\cq\1\earning'
file_names=os.listdir(file_dir)
file_paths=[os.path.join(file_dir,fn) for fn in file_names]
file_paths.sort(key=lambda x:int(x[-12:-4]))



csvfile=file(r'C:\cq\1\factor.csv','wb')
writer=csv.writer(csvfile)
title=open(r'C:\cq\1\format_earning.txt').read().split('\n')[0].split(',')
title+=['quarter','undefine','returns']
del title[15]
del title[14]
del title[1]
writer.writerow(title)
for fp in file_paths:
    date=int(fp[-12:-4])
    target_date=shift_date(date)
    lines=open(fp).read().split('\n')[:-1]
    for l in lines:
        items=l.split(',')
        stock=items[0]
        if stock in return_df_stocks:
            returns=return_df.loc[target_date,stock]
            items+=[returns]
            del items[15]
            del items[14]
            del items[1]
            writer.writerow(items)
    print fp[-12:-4]
csvfile.close()

factor_df=pd.read_csv(r'C:\cq\1\factor1.csv',index_col=0)
corr=factor_df.corr()
corr.to_csv(r'c:\cq\1\corr.csv')
