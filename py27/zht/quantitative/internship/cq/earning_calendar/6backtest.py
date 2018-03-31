# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 23:33:20 2016

@author: Administrator
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt


length=15
number=135


df=pd.read_csv(r'c:\marketAdjustedReturnDF_2004-2016.csv',index_col=0)
df_date=[d for d in df.index]

path=r'C:\earning_calendar\quarter'
files=os.listdir(path)
filesPath=[os.path.join(path,f) for f in files]
target_df=pd.DataFrame(np.zeros((len(df),len(df.T))),index=df.index,columns=df.columns)##initialize the target_df
target_df[target_df==0]=np.nan

date=[]
stock=[]
for i in range(len(filesPath)):
    line=open(filesPath[i]).read().split('\n')[:-1]
    date.extend([int(l[:8]) for l in line][:number])
    stock.extend([l[-9:] for l in line][:number])

for k in range(len(stock)):
    col=[s for s in df.columns]
    if stock[k] in col:#确保所选股票在df中
        stock_index=col.index(stock[k])####intersection
        for m in range(len(df_date)):
            if df_date[m]-date[k]<0 and df_date[m+1]-date[k]>=0:
                mark_date_index=m+1#发布季报后的第一个交易日（包含发布季报的当天）
                break
        for n in range(mark_date_index,len(df_date)):
            if str(df.iat[n,stock_index])!='nan':
                start_date_index=n
                break
        end_date_index=start_date_index+length
        for g in range(start_date_index,end_date_index+1):
            target_df.iat[g,stock_index]=df.iat[g,stock_index]
    print k
target_df=target_df.dropna(axis=1,how='all')
target_df.to_csv(r'C:\earning_calendar\target_df.csv')
returns=target_df.mean(axis=1)
returns=returns.fillna(0)
cum_sum=returns.cumsum()
cum_sum.to_csv(r'c:\earning_calendar\cum_sum1.csv')

fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot(cum_sum)
ticks=ax.set_xticks([0,242,484,725,967,1213,1475,1699,1934,2186,2424,2669,2913])
labels=ax.set_xticklabels(['2004','2005','2006','2007','2008','20009','2010','2011','2012','2013','2014','2015','2016'],rotation=30,fontsize='small')
ax.set_title('length=%d,number=%d'%(length,number))
fig.savefig(r'c:\earning_calendar\early\fig\%d_%d.png'%(length,number))
 


