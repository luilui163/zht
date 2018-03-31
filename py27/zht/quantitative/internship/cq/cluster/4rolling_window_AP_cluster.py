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
    day_paths=sorted(day_paths,key=lambda day_path:day_path[-8:])
    return day_paths

def paths_inside_window(date,window=500):
    day_paths=get_paths(r'C:\bloomberg_new\bloomberg')
    if not os.path.isdir(r'c:\cluster\result\%d'%date):
        os.makedirs(r'c:\cluster\result\%d'%date)
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

def AP_cluster(return_df,date):    
    df=return_df.fillna(0).T
    stocks=[d for d in df.index]
    X=np.array(df)
    af=AffinityPropagation().fit(X)
    labels=af.labels_
#    if not os.path.isdir(r'/home/hzhang/cluster/%d'%date):
#        os.makedirs(r'/home/hzhang/cluster/%d'%date)
    for l in range(labels.max()+1):
        f=open(r'c:\cluster\result\%d\%d.txt'%(date,l),'w')
        for i in range(len(labels)):
            if labels[i]==l:
                f.write('%s\n'%stocks[i])
        f.close()

def start(date):
    paths=paths_inside_window(date)
    closeprice_df=get_closeprice_df(paths)
    return_df=get_return_df(closeprice_df)
    AP_cluster(return_df,date)



dates=open(r'C:\cluster\dates.txt').read().split('\n')[:-1][72:]
for i in range(len(dates)):
    start(int(dates[i]))
    print dates[i],time.time()-tmp_time
    tmp_time=time.time()





