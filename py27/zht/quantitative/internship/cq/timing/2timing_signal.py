# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 23:33:20 2016

@author: Administrator
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
import time

path=r'C:\bloomberg_new\timing'
files=os.listdir(path)
files_paths=[os.path.join(path,f) for f in files]
files_paths=sorted(files_paths,key=lambda x:int(x[-12:-4]))

def get_rank(files_number,files_paths):
    i=files_number
    variables=[]
    for v in range(i-window,i):
        variables.append(float(open(files_paths[v]).read().split('\n')[0].split('\t')[0]))
    v_tmp=sorted(variables,reverse=True)
    rank=v_tmp.index(variables[-1])
    return rank

def get_rank_list(files_paths):
    dates=[]
    ranks=[]
    for i in range(window,len(files_paths)):
        dates.append(files_paths[i][-12:-4])
        ranks.append(get_rank(i,files_paths))
    return (dates,ranks)


def get_target_dates(dates,ranks):
    target_dates=[]
    for j in range(len(dates)):
        if float(ranks[j])/window<=thresh:
            target_dates.append(int(dates[j]))
    return target_dates


def get_pnl(target_dates):
    df=pd.read_csv(r'c:\market_return_2004-2016.csv',index_col=0)
    index_dates=[k for k in df.index]
    pnl=[0]*len(df)
    for i in range(len(target_dates)):
        if target_dates[i] in index_dates:
            index=index_dates.index(target_dates[i])
            pnl[index]=df.iat[index,0]
    pnl=pd.DataFrame(pnl,index_dates)
    return pnl


def draw(pnl):
    std=pnl.std()
    cum_sum=pnl.cumsum()
    informationRatio=cum_sum.values[-1]/std
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.plot(cum_sum)
    ax.set_xticks([0,242,484,725,967,1213,1475,1699,1934,2186,2424,2669,2913])
    ax.set_xticklabels(['2004','2005','2006','2007','2008','20009','2010','2011','2012','2013','2014','2015','2016'],rotation=30,fontsize='small')
    ax.set_title('window=%d,thresh=%.2f,informationRatio=%f'%(window,thresh,informationRatio))
    fig.savefig(r'C:\bloomberg_new\fig\window=%d,thresh=%.2f.png'%(window,thresh))




start=time.time()
window=20
thresh=0.3
for window in [5,10,20,30,50]:
    for thresh in [0.1,0.2,0.3,0.5,0.8]:
        (dates,ranks)=get_rank_list(files_paths)
        target_dates=get_target_dates(dates,ranks)
        pnl=get_pnl(target_dates)
        draw(pnl)
        print time.time()-start
        start=time.time()
    
    
    
    
    
    
    
    