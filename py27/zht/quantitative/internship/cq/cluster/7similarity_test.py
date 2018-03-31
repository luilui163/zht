# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 11:02:33 2016

@author: Administrator
"""

import os
import numpy as np
import pandas as pd


def get_valid_clusters_paths(index,path):
    dates=os.listdir(path)
    dates_paths=[os.path.join(path,d) for d in dates]
    i=index
    clusters=os.listdir(dates_paths[i])
    clusters_paths=[os.path.join(dates_paths[i],cluster) for cluster in clusters]
    number=[0]*len(clusters)
    for c in range(len(clusters)):
        number[c]=len(open(clusters_paths[c]).read().split('\n')[:-1])
    valid_clusters_paths=[]
    for n in range(len(number)):
        if number[n]>=5 and number[n]<=50:
            valid_clusters_paths.append(clusters_paths[n])
    return valid_clusters_paths

def similarity(path1,path2):
    stock1=open(path1).read().split('\n')[:-1]
    stock2=open(path2).read().split('\n')[:-1]
    similarity=float(len(set(stock1).intersection(set(stock2))))/len(set(stock1).union(set(stock2)))
    return similarity

def get_avg(number1,number2,path):
    paths0=get_valid_clusters_paths(number1,path)
    paths1=get_valid_clusters_paths(number2,path)
    max_sim=[0]*len(paths0)
    for k in range(len(paths0)):
        sim=[0]*len(paths1)
        for m in range(len(paths1)):
            sim[m]=similarity(paths0[k],paths1[m])
        max_sim[k]=max(sim)
    avg=np.array(max_sim).mean()
    return avg
    
def get_similarity_df(path):
    dates=os.listdir(path)
    df=pd.DataFrame(np.zeros((len(dates),len(dates))),index=dates,columns=dates)
    for i in range(len(dates)):
        for j in range(len(dates)):
            df.iat[i,j]=get_avg(i,j,path)
            print i,j,get_avg(i,j,path)
    df.to_csv(r'c:\cluster\similarity_%s.csv'%path.split('\\')[-1])

#path=r'c:\cluster\APcluster'
#get_similarity_df(path)
path=r'C:\cluster\hcluster\ward300'
get_similarity_df(path)



















