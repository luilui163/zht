# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 13:24:50 2016

@author: Administrator
"""
import pandas as pd
import os
import time,datetime
import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import AgglomerativeClustering
import logging
import shutil
import re

tmp_time=time.time()

###
def get_paths(path):
    p=re.compile('\d{8}\Z')
    year_names=os.listdir(path)
    year_paths=[os.path.join(path,name) for name in year_names]
    month_paths=[]
    day_paths=[]
    for year_path in year_paths:
        month_names=os.listdir(year_path)
        for month_name in month_names:
            month_paths.append(os.path.join(year_path,month_name))
    for month_path in month_paths:
        day_names=os.listdir(month_path)
        for day_name in day_names:
            if bool(re.findall(p,day_name)):
                day_paths.append(os.path.join(month_path,day_name))
    day_paths=sorted(day_paths,key=lambda day_path:day_path[-8:])
    return day_paths

def paths_inside_window(date,window=500):
#    day_paths=get_paths(r'C:\cq\bloomberg')
    day_paths=get_paths(r'/dat/cqdata/marketdata/bloomberg')
    date_list=[int(p[-8:]) for p in day_paths]
    end_date_index=0
    start_date_index=0
    for i in range(len(date_list)-1):
        if date_list[i]<=date and date_list[i+1]>date:
            end_date_index=i
            start_date_index=i-window
            break
    paths_inside_window=day_paths[start_date_index:end_date_index]
    print len(paths_inside_window)
    return paths_inside_window


def get_closeprice_df_of_someday(day_paths,day_number):
    raw_lines=open(day_paths[day_number]).read().split('\n')
    lines=[]
    for l in range(len(raw_lines)):
        if len(raw_lines[l])!=0:#####挑选出A股
            if  raw_lines[l].split(',')[3][0]=='6' or raw_lines[l].split(',')[3][0]=='0' or raw_lines[l].split(',')[3][0]=='3':
                lines.append(raw_lines[l])

    stock_names=[line.split(',')[3] for line in lines]
    closeprice=[float(line.split(',')[5]) for line in lines]
    
    closeprice_df=pd.DataFrame({day_paths[day_number][-8:]:closeprice},index=stock_names)
    return closeprice_df
    
    
def get_closeprice_df(day_paths):
    closeprice_df=get_closeprice_df_of_someday(day_paths,0)
    for i in range(1,len(day_paths)):
#    for i in range(177,len(day_paths)):
        closeprice_df_i=get_closeprice_df_of_someday(day_paths,i)
#        closeprice_df=pd.concat([closeprice_df,closeprice_df_i],axis=1)
        closeprice_df=pd.merge(closeprice_df,closeprice_df_i,left_index=True,right_index=True,how='outer')
        print i
    return closeprice_df

def get_return_df(closeprice_df):
    closeprice_df=closeprice_df.T
    date=[d for d in closeprice_df.index][1:]
    i=0
    returns=np.diff(np.array(closeprice_df.iloc[:,i]))/np.array(closeprice_df.iloc[:,i])[:-1]
    return_df=pd.DataFrame({closeprice_df.columns[i]:returns},index=date)
    
    for i in range(1,len(closeprice_df.T)):
        returns=np.diff(np.array(closeprice_df.iloc[:,i]))/np.array(closeprice_df.iloc[:,i])[:-1]
        tmpDF=pd.DataFrame({closeprice_df.columns[i]:returns},index=date)
        return_df=pd.concat([return_df,tmpDF],axis=1)
    #adjust return_df
    return_df[return_df==0]=np.nan
    return_df=return_df.dropna(axis=1,thresh=200)
    return_df=return_df.fillna(0)
    return return_df

def AP_cluster(return_df,date):  
    df=return_df.fillna(0).T
    stocks=[d for d in df.index]
    X=np.array(df)
    af=AffinityPropagation().fit(X)
    labels=af.labels_
    count=[0]*(labels.max()+1)
    for i in range(labels.max()+1):
        for s in range(len(stocks)):
            if labels[s]==i:
                count[i]+=1
    f=open(r'/dat/cqdata/classification/cluster/affinity_cluster/%d.txt'%date,'w')
#    f=open(r'/home/hzhang/%d.txt'%date,'w')
#    f=open(r'c:\garbage\cluster\%d.txt','w')
    for s in range(len(stocks)):
        if count[labels[s]]>=3:
            f.write('%s\tap%d\n'%(stocks[s],labels[s]))
        else:
            f.write('%s\tap_odd\n'%stocks[s])
    f.close()
    print date

def H_cluster(return_df,date,industry_class='first',cluster_number=10,minimum_number=50,step=2):
    df=return_df.T
    df=df.fillna(0)
    stocks=[d for d in df.index]
    arr=np.array(df)
    flag=0
    for r in range(int(cluster_number*1.5),len(df)-500,step):
        print date,r,'step=',step
        agg=AgglomerativeClustering(n_clusters=r,linkage='ward').fit(arr)
        label=agg.labels_
        count=[0]*(label.max()+1)
        for i in range(label.max()+1):
            for s in range(len(stocks)):
                if label[s]==i:
                    count[i]+=1
        threshold=0
        flag=0
        for c in range(len(count)):
            if count[c]>minimum_number:
                threshold+=1
            if threshold>=cluster_number*0.9:
                flag=1
                break
        if flag==1:
            ticker=open(r'/dat/cqdata/classification/cluster/hierarchical_cluster/%s/%d.txt'%(industry_class,date),'w')
#            ticker=open(r'c:\garbage\cluster\%s\%d.txt'%(industry_class,date),'w')
            for s in range(len(stocks)):
                if count[label[s]]>=minimum_number:
                    ticker.write('%s\t%s_%d\n'%(stocks[s],industry_class,label[s]))
                else:
                    ticker.write('%s\t%s_odd\n'%(stocks[s],industry_class))
            ticker.close()
            print date,'is finished'
            break
    #继承，如果在指定的cluster_number,和minimum_number没有满足要求的分类，则放松条件继续分类，直到找到为止
    if flag==0:
        H_cluster(return_df,date,industry_class=industry_class,cluster_number=cluster_number-1,minimum_number=minimum_number-1,step=10)


def start(date):
    day_paths=paths_inside_window(date)
    closeprice_df=get_closeprice_df(day_paths)
    return_df=get_return_df(closeprice_df)
    AP_cluster(return_df,date)
    H_cluster(return_df,date,'first',10,45,2)
    H_cluster(return_df,date,'second',50,10,3)
    H_cluster(return_df,date,'third',100,5,5)
    H_cluster(return_df,date,'fourth',200,3,10)

def get_cluster_date():
    today=datetime.date.today()
    today_int=int(today.strftime('%Y%m%d'))
    year_and_month=today_int/100
    cluster_date=int(str(year_and_month)+'01')
    return cluster_date


if __name__=='__main__':
    date=get_cluster_date()
    start(date)




