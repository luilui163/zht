# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 15:37:42 2016

@author: hp
"""

import pandas as pd

return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)

lines=open(r'c:\cq\beta_exposure\exchange_rate.txt').read().split('\n')[:-3]
dates=[int(l.split('\t')[0]) for l in lines]
rates=[float(l.split('\t')[1]) for l in lines]

rate=pd.Series(rates,index=dates)

bp=rate.pct_change()*100

exchange_rate=pd.DataFrame({'rate':rates},index=dates)

exchange_rate.to_csv(r'c:\cq\beta_exposure\exchange_rate.csv')
exchange_rate_pct=exchange_rate.pct_change()
exchange_rate_pct.to_csv(r'c:\cq\beta_exposure\exchange_rate_pct.csv')
exchange_rate_diff=exchange_rate.diff()
exchange_rate_diff.to_csv(r'c:\cq\beta_exposure\exchange_rate_diff.csv')

lines=open(r'c:\cq\beta_exposure\shibor.txt').read().split('\n')[1:-3]
date=[int(l.split('\t')[0]) for l in lines]
on=[float(l.split('\t')[1]) for l in lines]
w1=[float(l.split('\t')[2]) for l in lines]
w2=[float(l.split('\t')[3]) for l in lines]
m1=[float(l.split('\t')[4]) for l in lines]
m2=[float(l.split('\t')[5]) for l in lines]
m3=[float(l.split('\t')[6]) for l in lines]
m6=[float(l.split('\t')[7]) for l in lines]
m12=[float(l.split('\t')[8]) for l in lines]
data={'on':on,
     'w1':w1,
     'w2':w2,
     'm1':m1,
     'm2':m2,
     'm3':m3,
     'm6':m6,
     'm12':m12
     }
shibor=pd.DataFrame(data,index=date)
shibor_pct=shibor.pct_change()
shibor_diff=shibor.diff()
shibor_diff.to_csv(r'c:\cq\beta_exposure\shibor_diff.csv')
shibor.to_csv(r'c:\cq\beta_exposure\shibor.csv')
shibor_pct.to_csv(r'c:\cq\beta_exposure\shibor_pct.csv')




