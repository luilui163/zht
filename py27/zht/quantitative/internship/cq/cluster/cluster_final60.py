# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 13:24:50 2016

@author: Administrator
"""


import pandas as pd
import os
import time
import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import AgglomerativeClustering
import logging
import shutil
import re

tmp_time=time.time()

###
def get_paths(path):
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
            day_paths.append(os.path.join(month_path,day_name))
    #remove   .dummy  files
    for d in range(len(day_paths)-1,-1,-1):
        if day_paths[d][-1] not in list([str(i) for i in range(10)]):
            day_paths.remove(day_paths[d])

    day_paths=sorted(day_paths,key=lambda day_path:day_path[-8:])
    return day_paths

def paths_inside_window(date,window=500):
    day_paths=get_paths(r'/home/hzhang/bloomberg_tmp')
    if not os.path.isdir(r'/home/hzhang/cluster/result2/%d'%date):
        os.mkdir(r'/home/hzhang/cluster/result2/%d'%date)
    date_list=[int(p[-8:]) for p in day_paths]
    end_date_index=0
    start_date_index=0
    for i in range(len(date_list)):
        if date_list[i]<=date and date_list[i+1]>date:
            end_date_index=i
            start_date_index=i-window
            break
    paths_inside_window=day_paths[start_date_index:end_date_index]
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
        closeprice_df_i=get_closeprice_df_of_someday(day_paths,i)
        closeprice_df=pd.concat([closeprice_df,closeprice_df_i],axis=1)
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
'''
def AP_cluster(return_df,date):
    return_df=return_df.iloc[:,:10]#######
    edge_model=covariance.GraphLassoCV()
    edge_model.fit(return_df)
#    os.mkdir(r'c:\cluster\result2\%d'%local_date)
    _,labels = cluster.affinity_propagation(edge_model.covariance_)
    n_labels=labels.max()

    for i in range(n_labels+1):
        f=open(r'/home/hzhang/cluster/result2/%d/%d.txt'%(date,i),'w')
        for j in range(len(return_df.columns[labels==i])):
            f.write('%s\n'%return_df.columns[labels==i][j])
        f.close()
'''    

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
    f=open(r'/dat/datadev/workspace/classification/affinity_cluster/%d.txt'%date,'w')
    for s in range(len(stocks)):
        if count[labels[s]]>=3:
            f.write('%s\tap%d\n'%(stocks[s],labels[s]))
        else:
            f.write('%s\tap_odd\n'%stocks[s])
    f.close()
    print date
'''
def H_cluster(return_df,date,cluster_number=10,minimum_number=50):
    df=return_df.T
    df=df.fillna(0)
    stocks=[d for d in df.index]
    arr=np.array(df)
    for r in [cluster_number*2] :
        logging.info('cluster_number=',cluster_number,r)
        agg=AgglomerativeClustering(n_clusters=r,linkage='ward').fit(arr)
        label=agg.labels_
        count=[0]*(label.max()+1)
        for i in range(label.max()+1):
            for s in range(len(stocks)):
                if label[s]==i:
                    count[i]+=1
        ticker=open(r'c:\cluster\hcluster\%d\%d.txt'%(cluster_number,date),'w')
        for s in range(len(stocks)):
            if count[label[s]]>=minimum_number:
                ticker.write('%s\t%d_h%d\n'%(stocks[s],cluster_number,label[s]))
            else:
                ticker.write('%s\t%d_odd\n'%(stocks[s],cluster_number))
        ticker.close()
'''
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
            ticker=open(r'/dat/datadev/workspace/classification/hierarchical_cluster/%s/%d.txt'%(industry_class,date),'w')
            for s in range(len(stocks)):
                if count[label[s]]>=minimum_number:
                    ticker.write('%s\t%s_%d\n'%(stocks[s],industry_class,label[s]))
                else:
                    ticker.write('%s\t%s_odd\n'%(stocks[s],industry_class))
            ticker.close()
            print date,'is finished'
            break
    #如果在指定的cluster_number,和minimum_number没有满足要求的分类，则放松条件继续分类，直到找到为止
    if flag==0:
        H_cluster(return_df,date,industry_class=industry_class,cluster_number=cluster_number-1,minimum_number=minimum_number-1,step=10)


def start(date):
    paths=paths_inside_window(date)
    closeprice_df=get_closeprice_df(paths)
    return_df=get_return_df(closeprice_df)
    AP_cluster(return_df,date)
    H_cluster(return_df,date,'first',10,45,2)
    H_cluster(return_df,date,'second',50,10,3)
    H_cluster(return_df,date,'third',100,5,5)
    H_cluster(return_df,date,'fourth',200,3,10)

if os.path.isdir(r'/home/hzhang/bloomberg_tmp'):
    shutil.rmtree(r'/home/hzhang/bloomberg_tmp')
shutil.copytree(r'/dat/datadev/workspace/bloomberg',r'/home/hzhang/bloomberg_tmp')
if os.path.isfile(r'/home/hzhang/bloomberg_tmp/2010/05/RAWPRICES.20100510a'):
    os.remove(r'/home/hzhang/bloomberg_tmp/2010/05/RAWPRICES.20100510')
    os.rename(r'/home/hzhang/bloomberg_tmp/2010/05/RAWPRICES.20100510a',r'/home/hzhang/bloomberg_tmp/2010/05/RAWPRICES.20100510')


dates=open(r'/home/hzhang/cluster/dates.txt').read().split('\n')[:-1][:60]
for i in range(len(dates)):
    start(int(dates[i]))
    print dates[i],time.time()-tmp_time
    tmp_time=time.time()

shutil.rmtree(r'/home/hzhang/bloomberg_tmp')



