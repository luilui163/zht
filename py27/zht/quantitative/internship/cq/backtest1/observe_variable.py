# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 16:28:51 2016

@author: hp
"""
import pandas as pd
import numpy as np
from util import *
import matplotlib.pyplot as plt
from process_data import Variable
import os


dd=open(r'data.txt').read().split('\n')[:-1]
name=dd[0].split('\t')
datatype=dd[1].split('\t')
data=[r.split('\t') for r in dd[2:]]
cols=zip(name,range(len(name)),datatype)
variables=[Variable(c[0],c[1],c[2]) for c in cols if c[2] in ['c','d']]

#data=open('data.txt').read().split('\n')[:-1]
#lines=open('data_description.txt').read().split('\n')[:-1]
#colnames=[tuple(l.split('\t')) for l in lines]
#variables=[Variable(colnames[i][0],colnames[i][1],colnames[i][2]) for i in range(len(colnames))]

class Category:
    def __init__(self):
        pass


def continuous_category(variable):
    raw_values=open('c\%s.txt'%variable.name).read().split('\n')[:-1]
    values=[float(v) for v in raw_values]

    categorys=[]
    for i in range(len(values)-1):
        category=Category()
        category.id=i
        category.name='['+str(values[i+1])+','+str(values[i])+')'
        category.alpha=[]
        for d in data:
            try:
                if values[i+1]<float(d[variable.col])<values[i]:
                    stock=d[0]
                    start_date=shift_date(d[1])
                    end_date=shift_date(start_date,1)
                    category.alpha.append((stock,start_date,end_date,1))
            except:
                pass
        category.pnl=position_to_pnl(alpha_to_position(category.alpha))
        categorys.append(category)
        print values[i]
    return categorys

def discrete_category(variable):
    raw_values=open(r'd\%s.txt'%variable.name).read().split('\n')[:-1]
    #some categorys' sample is too small,a threshold(100) is set,
    #means that we just observe those category with samples more than 100
    values=[v.split('\t')[0] for v in raw_values if int(v.split('\t')[1])>100]
    
    categorys=[]
    for i in range(len(values)):
        category=Category()
        category.id=i
        category.name=values[i]
        category.alpha=[]
        for d in data:
            if d[variable.col]==values[i]:
                stock=d[0]
                start_date=shift_date(d[1])
                end_date=shift_date(start_date,1)
                category.alpha.append((stock,start_date,end_date,1))
    
        category.pnl=position_to_pnl(alpha_to_position(category.alpha))
        categorys.append(category)
        print values[i]
    return categorys


def plot2(variable):
    if variable.datatype=='c':
        categorys=continuous_category(variable)
    elif variable.datatype=='d':
        categorys=discrete_category(variable)
    pnls={}
    for category in categorys:
        pnls[category.id]=category.pnl
    
    pnl_df=pd.DataFrame(pnls)
    
    e=0
    for i in range(len(pnl_df)):
        flag=0
        for j in range(len(pnl_df.columns)):
            if pd.notnull(pnl_df.iat[i,j]):
                flag=1
                break
        if flag:
            e=i
            break
        
    pnl_df=pnl_df.iloc[e:]
    count=pnl_df[pd.notnull(pnl_df)].count()
    positive=pnl_df[pnl_df>0].count()
    win_rate=positive/count
    
    #information ratio
    pnl_df.iloc[0]=0
    std=pnl_df.std()
    avg=pnl_df.mean()
    information_ratio=avg/std
    
    #win_rate
    count=pnl_df[pd.notnull(pnl_df)].count()
    positive=pnl_df[pnl_df>0].count()
    win_rate=positive/count
    
    pnl_df=pnl_df.fillna(0)
    cum_sum=pnl_df.cumsum()
    fig,ax=plt.subplots(1,1,figsize=(12,8))
    #fig=plt.figure()
    #ax=fig.add_subplot(1,1,1)
    ax.plot(cum_sum)
    
    year=[y/10000 for y in list(cum_sum.index)]
    xticks=[]
    xticklabels=[]
    for i in range(1,len(year)):
        if year[i]>year[i-1]:
            xticks.append(i)
            xticklabels.append(str(year[i]))
            
    if len(xticks)<3:
        year=[y/100 for y in list(cum_sum.index)]
        xticks=[]
        xticklabels=[]
        for i in range(1,len(year)):
            if year[i]>year[i-1]:
                xticks.append(i)
                xticklabels.append(str(year[i]))
            
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels,rotation=90,fontsize='small')

    plt.legend(tuple(pnl_df.columns),loc='upper left')
    plt.title(variable.name)
    
    if not os.path.isdir('observe_variable'):
        os.makedirs('observe_variable')
    
    figname=r'observe_variable\%s.png'%variable.name
    fig.savefig(figname)
    
    description=[(categorys[i].name,information_ratio[i],win_rate[i]) for i in range(len(categorys))]
    description.sort(key=lambda x:x[1],reverse=True)
    
    with open('observe_variable\%s_description.txt'%variable.name,'w') as f:
        for des in description:
            f.write('%s\t%f\t%f\n'%des)


def run():
    for variable in variables:
        plot2(variable)
        print variable.name


run()
    