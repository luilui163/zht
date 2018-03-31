# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 23:33:20 2016

@author: Administrator
"""
import pandas as pd

path=r'c:\closeprice_df2004-2016.csv'
df=pd.read_csv(path,index_col=0)
marked_stocks=[]
for j in range(len(df.T)):
    tmpdf=df.iloc[:,j]
    tmpdf=tmpdf.dropna()
    if len(tmpdf.index)<50:
        marked_stocks.append(df.columns[j])

for marked_stock in marked_stocks:
    del df[marked_stock]
df.to_csv(r'c:\cluster\closeprice_df.csv')





path1=r'c:\openprice_df2004-2016.csv'
df1=pd.read_csv(path1,index_col=0)
marked_stocks1=[]
for j1 in range(len(df1.T)):
    tmpdf1=df1.iloc[:,j1]
    tmpdf1=tmpdf1.dropna()
    if len(tmpdf1.index)<50:
        marked_stocks1.append(df1.columns[j])

for marked_stock1 in marked_stocks1:
    del df1[marked_stock1]
df1.to_csv(r'c:\cluster\openprice_df.csv')