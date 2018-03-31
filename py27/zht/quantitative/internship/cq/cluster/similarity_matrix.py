# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 16:09:14 2016

@author: Administrator
"""
import os
import pandas as pd
import numpy as np

def similarity(path1,path2):
    stock1=open(path1).read().split('\n')[:-1]
    stock2=open(path2).read().split('\n')[:-1]
    if len(set(stock1).union(set(stock2)))==0:
        similarity=0
    else:
        similarity=float(len(set(stock1).intersection(set(stock2))))/len(set(stock1).union(set(stock2)))
    return similarity

def get_paths(c):
    path=r'c:\cluster\similarity\%s'%c
    files=os.listdir(path)
    files_paths=[os.path.join(path,f)for f in files]
    return files_paths
    
def get_industrys(c):
    path=r'c:\cluster\similarity\%s'%c
    files=os.listdir(path)
    industrys=[f[:-4] for f in files]
    return industrys

name=['ap','bbg','gx','wind','zx']
paths=[0]*len(name)
industrys=[0]*len(name)
for h in range(len(name)):
    paths[h]=get_paths(name[h])
    industrys[h]=get_industrys(name[h])

similarity_matrix=pd.DataFrame(np.zeros((len(name),len(name))),index=name,columns=name)
for t in range(len(name)):
    for y in range(len(name)):
        df=pd.DataFrame(np.zeros((len(paths[t]),len(paths[y]))),index=industrys[t],columns=industrys[y])
        for i in range(len(paths[t])):
            for j in range(len(paths[y])):
                df.iat[i,j]=similarity(paths[t][i],paths[y][j])
        print t,y
        similarity_matrix.iat[t,y]=df.max().mean()
similarity_matrix.to_csv(r'c:\cluster\similarity\similarity_matrix.csv')



