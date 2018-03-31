# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 10:01:35 2016

@author: hp
"""
import pandas as pd

def get_data_list_and_stock_name_list(col):
    data_list=[]
    stock_list=[]
    years=range(2005,2016)
    for year in years:
        lines=open(r'c:\cq\salary\%d.txt'%year).read().split('\n')[:-1]
        stock=[l.split('\t')[0] for l in lines]
        data=[float(l.split('\t')[col]) for l in lines]
        data_list.append(data)
        stock_list.append(stock)
    return data_list,stock_list,years



def get_data_df(col):
    closeprice_list,stock_name_list,dates=get_data_list_and_stock_name_list(col)
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

#dat_df=get_data_df()
def get_final_data_df(col):
    data_df=get_data_df(col)
    absolute_growing_df=data_df-data_df.shift(1)
    relative_growing_df=(data_df-data_df.shift(1))/data_df.shift(1)
    
    data_df.to_csv(r'C:\cq\salary\data_df%d.csv'%col)
    absolute_growing_df.to_csv(r'C:\cq\salary\absolute_growing_df%d.csv'%col)
    relative_growing_df.to_csv(r'C:\cq\salary\relative_growing_df%d.csv'%col)

for i in range(1,4):
    get_final_data_df(i)




