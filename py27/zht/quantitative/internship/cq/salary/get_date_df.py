# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 10:01:35 2016

@author: hp
"""
import pandas as pd
import numpy as np

def get_data_list_and_stock_name_list():
    data_list=[]
    stock_list=[]
    years=range(2004,2016)
    for year in years:
        lines=open(r'c:\cq\salary\%d.txt'%year).read().split('\n')[:-1]
        stock=[l.split('\t')[0] for l in lines]
        data=[float(l.split('\t')[5]) for l in lines]
        data_list.append(data)
        stock_list.append(stock)
    return data_list,stock_list,years



def get_data_df():
    closeprice_list,stock_name_list,dates=get_data_list_and_stock_name_list()
    i=0
    df0=pd.DataFrame(closeprice_list[i],index=stock_name_list[i],columns=[dates[i]])
    for i in range(1,len(stock_name_list)):
        df1=pd.DataFrame(closeprice_list[i],index=stock_name_list[i],columns=[dates[i]])
        df=pd.concat([df0,df1],axis=1)
        df0=df
        print i,dates[i]
#    df.T.to_csv()
#    df[df==float('nan')]=np.NaN
    return df.T
    
df=get_data_df()
df.to_csv(r'c:\cq\salary\date_df.csv')
