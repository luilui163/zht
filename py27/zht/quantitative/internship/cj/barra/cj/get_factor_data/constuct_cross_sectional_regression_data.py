#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
import os



directory=r'C:\data\cj\final_data'
factor_names=os.listdir(directory)

date_intersection=[]
for i,fn in enumerate(factor_names):
    file_names=os.listdir(os.path.join(directory,fn))
    dates=[fn[:10] for fn in file_names]
    if i == 0:
        date_intersection=dates
    else:
        date_intersection=[d for d in date_intersection if d in dates]


for date in date_intersection:
    cross_sectional_df=pd.DataFrame()
    for factor in factor_names:
        file_path=os.path.join(directory,factor,date+'.csv')
        tmp_df=pd.read_csv(file_path,index_col=0)
        tmp_df.columns=[factor]
        cross_sectional_df=cross_sectional_df.append(tmp_df.iloc[:,0])
    print date
    cross_sectional_df = cross_sectional_df.T
    cross_sectional_df.to_csv(r'C:\data\cj\cross_data\%s.csv'%date)


#add the returns columnn to df
returns_df=pd.read_csv(r'C:\data\gx\csvdata\month_returns.csv',index_col=0)
returns_df=returns_df.shift(1)
returns_df.index=[pd.to_datetime(ind) for ind in returns_df.index]
path=r'c:\data\cj\cross_data'
filenames=os.listdir(path)
for fn in filenames:
    df=pd.read_csv(os.path.join(path,fn),index_col=0)
    df.index=[ind[:6] for ind in df.index]
    date=fn[:-4].decode('utf8')
    returns=returns_df.loc[date[:7]]
    df['returns']=returns.T
    print fn
    df.to_csv(r'C:\data\cj\cross_data2\%s.csv'%date)



#adjust the liq_market_value
path=r'c:\data\cj\cross_data2'
filenames=os.listdir(path)
for fn in filenames:
    df=pd.read_csv(os.path.join(path,fn),index_col=0)
    liq_df=pd.read_csv(os.path.join(r'C:\data\cj\liq_market_value',fn),index_col=0)
    liq_df=liq_df[:-1] # the last row does not belong to A share
    liq_df.index=[int(ind[:6]) for ind in liq_df.index]
    df['liq_market_value']=liq_df.iloc[:,0]

    df.to_csv(os.path.join(r'C:\data\cj\cross_data3',fn))
    print fn
















