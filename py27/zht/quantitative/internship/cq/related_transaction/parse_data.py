# -*- coding: utf-8 -*-
"""
Created on Thu Aug 04 11:25:41 2016

@author: hp
"""

import pandas as pd


#for i in range(1,7):  
#    data1=pd.read_csv(R'C:\cq\related_transaction\%d.csv'%i,index_col=0)
#    annual_1=data1.iloc[range(3,52,4)]
#    annual_1.to_csv(r'C:\cq\related_transaction\annual_%d.csv'%i)
#    semi_1=data1.iloc[range(1,50,4)]
#    semi_1.to_csv(r'C:\cq\related_transaction\semi_%d.csv'%i)

for i in range(1,7):
    data=pd.read_csv(R'c:\cq\related_transaction\annual_%d.csv'%i ,index_col=0)
    data=data[data>0]
    df=(data-data.shift(1))/data.shift(1)
    df.to_csv(r'c:\cq\related_transaction\annual_growing_relative_%d.csv'%i)









