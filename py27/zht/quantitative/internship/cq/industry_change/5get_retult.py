# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:33:19 2016

@author: Administrator
"""
import os
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

start=time.time()


#path=r'C:\industry_change\zx'
#
#files=os.listdir(path)
#files_paths=[os.path.join(path,f) for f in files]
#files_paths=sorted(files_paths)


def handle_one_file(file_number,files_paths):
    i=file_number
    date=0
    lines=open(files_paths[i]).read().split('\n')[:-1]
    stock=files_paths[i].split('_')[2][-9:]
    for j in range(2,len(lines)-1):
#        date0=lines[j-1].split('\t')[0]
        industry0=lines[j-1].split('\t')[1].split('-')[2]
        date1=lines[j].split('\t')[0]
        industry1=lines[j].split('\t')[1].split('-')[2]
        if industry1!=industry0:
            date=date1
            break
    return (stock,date,industry0,industry1)

def get_stocks_and_dates():
    path=r'C:\industry_change\zx_new'
    files=os.listdir(path)
    files_paths=[os.path.join(path,f) for f in files]
    files_paths=sorted(files_paths)
    
    stocks=[]
    dates=[]
    industrys0=[]
    industrys1=[]
    for m in range(len(files_paths)):
        (stock,date,industry0,industry1)=handle_one_file(m,files_paths)
        stocks.append(stock)
        dates.append(date)
        industrys0.append(industry0)
        industrys1.append(industry1)
    return (stocks,dates,industrys0,industrys1)

(stocks,dates,industrys0,industrys1)=get_stocks_and_dates()


def get_pnl(stocks,dates,length,time_model):
    #time_model   -1 for before    1 for after
    df=pd.read_csv(r'c:\returnDF_2004-2016.csv',index_col=0)
    market_return=df.mean(axis=1)
    df_index=[i for i in df.index]
    df_col=[c for c in df.columns]
    #target_df=pd.DataFrame(np.nan((len(df),len(df.T))),index=[i for i in df.index],columns=[c for c in df.columns])
    target_df=df.copy()
    target_df[target_df>-9999999]=np.nan
    for i in range(len(stocks)):
        if dates[i]!=0:
            index=df_index.index(int(dates[i]))
            col=df_col.index(stocks[i])
            if abs(df.iat[index,col])<=0.095:
                if time_model==-1:
                    for k in range(index-length,index):
                        target_df.iat[k,col]=-df.iat[k,col]+market_return.values[k]
                if time_model==1:
                    for k in range(index,index+length):
                        target_df.iat[k,col]=-df.iat[k,col]+market_return.values[k]
    target_df.to_csv(r'C:\industry_change\%d.csv'%length)
    pnl=target_df.mean(axis=1)
    return pnl


def draw(pnl,length,time_model):
    pnl=pnl.fillna(0)
    std=pnl.std()
    avg=pnl.mean()
    pnl.to_csv(r'c:\industry_change\pnl_%d.csv'%length)
    cum_sum=pnl.cumsum()
    cum_sum.to_csv(r'c:\industry_change\cumsum_%d.csv'%length)
    informationRatio=avg/std
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.plot(cum_sum)
    ax.set_xticks([0,242,484,725,967,1213,1475,1699,1934,2186,2424,2669,2913])
    ax.set_xticklabels(['2004','2005','2006','2007','2008','20009','2010','2011','2012','2013','2014','2015','2016'],rotation=30,fontsize='small')
    if time_model==-1:
        ax.set_title('before,length=%d,informationRatio=%f'%(length,informationRatio))
        fig.savefig(r'C:\industry_change\fig\before\length=%d.png'%(length))
    if time_model==1:
        ax.set_title('after,length=%d,informationRatio=%f'%(length,informationRatio))
        fig.savefig(r'C:\industry_change\fig\after\length=%d.png'%(length))

for time_model in [-1,1]:
    for length in [50]:
        pnl=get_pnl(stocks,dates,length,time_model)
        draw(pnl,length,time_model)
        print length,time_model,time.time()-start
        start=time.time()




