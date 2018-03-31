# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 13:33:19 2016

@author: Administrator
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
'''
找到相对发布日期较早的方法：
1,发布日期的时间在当前已经发布的季报时间排序中的index_number小于上一季度的index_number days天以上。
  等价于当个季报时间范围内所有dates排序中的index_number,早days
2,如果某只股票发布了多次季报，且都满足上面的条件，则有可能在某个季度被多次持有
'''
start=time.time()

def get_index_number(path):
    lines=open(path).read().split('\n')[:-1]
    dates=[l.split('\t')[0] for l in lines]
    stocks=[l.split('\t')[1] for l in lines]
    dates_set_list=sorted(list(set([int(d) for d in dates])))
    index_numbers=[0]*len(stocks)
    for i in range(len(stocks)):
        index_numbers[i]=dates_set_list.index(int(dates[i]))
#    for j in range(20):
#        print j,index_numbers[j],stocks[j]
    return (index_numbers,dates,stocks)

def get_target_stocks_and_dates_of_one_quarter(path_of_quarter,days,time_model):
    path=path_of_quarter
    files=os.listdir(path)
    files_paths=[os.path.join(path,f) for f in files]
    files_paths=sorted(files_paths,key=lambda p:p[-10:-6])
    target_stocks=[]
    target_dates=[]
    for i in range(1,len(files_paths)):
        (index_numbers1,dates1,stocks1)=get_index_number(files_paths[i])
        (index_numbers0,dates0,stocks0)=get_index_number(files_paths[i-1])
    #    intersection_stocks=list(set(stocks1).intersection(set(stocks0)))
        for k in range(len(stocks1)):####因为df1中有重复的stock，导致pd.concat 用不了
            if time_model=='earlier':
                if stocks1[k] in stocks0 and index_numbers0[stocks0.index(stocks1[k])]-index_numbers1[k]>=days:#############short <=-2 or  long >=2
                    target_stocks.append(stocks1[k])
                    target_dates.append(dates1[k])
            if time_model=='later':
                if stocks1[k] in stocks0 and index_numbers1[k]-index_numbers0[stocks0.index(stocks1[k])]>=days:#############short <=-2 or  long >=2
                    target_stocks.append(stocks1[k])
                    target_dates.append(dates1[k])
    return (target_stocks,target_dates)
        
def get_all_target_stocks_and_dates(days,time_model):
    (target_stocks,target_dates)=get_target_stocks_and_dates_of_one_quarter(r'c:\earning_calendar\relative\Q1',days,time_model)
    for q in range(2,5):
        path_of_quarter=r'c:\earning_calendar\relative\Q%d'%q
        (tmp_target_stocks,tmp_target_dates)=get_target_stocks_and_dates_of_one_quarter(path_of_quarter,days,time_model)
        target_stocks.extend(tmp_target_stocks)
        target_dates.extend(tmp_target_dates)
    return(target_stocks,target_dates)


def get_result(target_stocks,target_dates,days,length,time_model,trade_model):
    date=[int(d) for d in target_dates]
    stock=target_stocks

    df=pd.read_csv(r'c:\returnDF_2004-2016.csv',index_col=0)
#    df=pd.read_csv(r'c:\marketAdjustedReturnDF_2004-2016.csv',index_col=0)
    df_date=[d for d in df.index]
    target_df=pd.DataFrame(np.zeros((len(df),len(df.T))),index=df.index,columns=df.columns)##initialize the target_df
    target_df[target_df==0]=np.nan
    
    f=open(r'C:\earning_calendar\relative\correlation\days_%d.txt'%days,'w')
    for k in range(len(stock)):
        col=[s for s in df.columns]
        if stock[k] in col:#确保所选股票在df中
            stock_index=col.index(stock[k])####intersection
            for m in range(len(df_date)):
                if df_date[m]-date[k]<0 and df_date[m+1]-date[k]>=0:
                    mark_date_index=m+1#发布季报后的第一个交易日（包含发布季报的当天）
                    break
        if str(df.iat[mark_date_index-1,stock_index])!='nan' and str(df.iat[mark_date_index,stock_index])!='nan':
            f.write('%f\t%f\n'%(float(df.iat[mark_date_index,stock_index]),float(df.iat[mark_date_index-1,stock_index])))
    f.close()
    

for days in [1,3,10,20]:
    for length in [1]:
        for time_model in ['earlier']:
            for trade_model in ['long']:
                (target_stocks,target_dates)=get_all_target_stocks_and_dates(days,time_model)# trade_model:1 for long ,-1 for short
                get_result(target_stocks,target_dates,days,length,time_model,trade_model)
        print days,length

end=time.time()
print end-start

