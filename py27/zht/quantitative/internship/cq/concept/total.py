# -*- coding: utf-8 -*-
"""
Created on Mon Jul 04 11:26:14 2016

@author: 13163
"""
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

start_date=20160104
cap_df=pd.read_csv(r'c:\cq\cap_df.csv',index_col=0)
return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)



def get_index_df(concept,path):
    sid=open(path).read().split('\n')[:-1]
    stock_names=[c for c in cap_df.columns]
    
    dates=list(cap_df.index)
    mark=dates.index(start_date)
    
    target_stocks=[stock_name for stock_name in stock_names if stock_name[:6] in sid]
    #因为有些交易日，股票数据可能因为停牌等缺失，这里先向前填充，然后向后填充
    
    target_df=cap_df[target_stocks]
    target_df=target_df.fillna(method='pad')
    target_df=target_df.fillna(method='bfill')
    total=target_df.sum(axis=1)
    tmp=total/total.values[mark]*1000
    index=tmp.iloc[mark:]
    index_df=pd.DataFrame(index,columns=[concept])
    return index_df

def get_df():
    folder=r'C:\cq\concept\wind_new\%d'%start_date
    file_name=os.listdir(folder)
    concepts=[ff[:-4] for ff in file_name]
    file_path=[os.path.join(folder,f) for f in file_name]
    
    index0=get_index_df(concepts[0],file_path[0])
    for i in range(1,len(concepts)):
        index1=get_index_df(concepts[i],file_path[i])
        df=pd.concat([index0,index1],axis=1)
        index0=df
        print i,concepts[i]
    
    index_df=index0
#    index_df.to_csv(r'c:\garbage\wind\index_df.csv')
    index_return_df=(index0-index0.shift(1))/index0
#    index_return_df.to_csv(r'c:\garbage\wind\index_return_df.csv')
    
    index_rolling_return_mean_df=pd.rolling_mean(index_return_df,ma)
#    index_rolling_return_mean_df.to_csv(r'c:\garbage\wind\index_rolling_return_mean_df.csv')    
    
    index_rolling_return_std_df=pd.rolling_std(index_return_df,ma)
#    index_rolling_return_std_df.to_csv(r'c:\garbage\wind\index_rolling_return_std_df.csv')
    
    return index_df,index_return_df,index_rolling_return_mean_df,index_rolling_return_std_df
    

index_df,index_return_df,index_rolling_return_mean_df,index_rolling_return_std_df=get_df()




def get_concepts_list():
#    df=pd.read_csv(r'c:\garbage\wind\index_rolling_return_std_df.csv',index_col=0)
    index_df,index_return_df,index_rolling_return_mean_df,index_rolling_return_std_df=get_df()
    ###############################
    df=index_rolling_return_std_df
    ###############################
    concept_number=len(df.columns)
    target_number=int(concept_number*ratio)+1
    
    concepts_list=[]
    for i in range(len(df.index)):
        tmp_row=df.iloc[i]
        row_list=list(tmp_row)
        
        
        ########这里代码有问题，tmp_index一直在变，有问题，要是绝对index
        target_concept=[]
        for t in range(target_number):
            tmp_max=max(row_list)
            tmp_index=row_list.index(tmp_max)
            target_concept.append(df.columns[tmp_index])
            row_list.remove(tmp_max)
        concepts_list.append(target_concept)
    '''因为是根据T的信号决定T+1的建仓，故日期需要向前shift'''
    return list(df.index)[2:],concepts_list[1:-1]

def get_target_df():
    dates,concepts_list=get_concepts_list()
    
    target_df=pd.DataFrame(np.zeros((len(dates),len(return_df.columns))),index=dates,columns=return_df.columns)##initialize the target_df
    target_df[target_df==0]=np.nan
    stocks_of_df=list(return_df.columns)
    
    for i in range(len(concepts_list)):
        target_stocks_of_one_day=[]
        concepts_of_one_day=concepts_list[i]
        for c in concepts_of_one_day:
            #因为考虑到后边有些概念可能消失了，会找不到对应的文件记录
            try:
                stocks=open(r'c:\cq\concept\wind_new\%d\%s.txt'%(dates[i],c)).read().split('\n')[:-1]
            except IOError:
                pass
            
            for s in stocks_of_df:
                if s[:6] in stocks:
                    target_stocks_of_one_day.append(s)
        
        row_index1=list(target_df.index).index(dates[i])
        row_index2=list(return_df.index).index(dates[i])
        for t in target_stocks_of_one_day:
            col_index=list(return_df.columns).index(t)
            target_df.iat[row_index1,col_index]=return_df.iat[row_index2,col_index]
        print dates[i]
    return target_df

def get_fig():
    target_df=get_target_df()

    tmp_df=return_df.iloc[list(return_df.index).index(list(target_df.index)[0]):]
    pnl=target_df.mean(axis=1)-tmp_df.mean(axis=1)
    std=pnl.std()
    avg=pnl.mean()
    cum_sum=pnl.cumsum()
    information_ratio=avg/std
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.plot(cum_sum)
    
    ax.plot(cum_sum)
    month=[y/100 for y in list(cum_sum.index)]
    xticks=[]
    xticklabels=[]
    for i in range(1,len(month)):
        if month[i]>month[i-1]:
            xticks.append(i)
            xticklabels.append(str(month[i]))
    ax.set_xticks(xticks)
    ax.set_title('IR=%f'%information_ratio)
    ax.set_xticklabels(xticklabels,rotation=90,fontsize='small')
    fig.savefig(r'c:\garbage\wind\%d_ma_%d_ratio_%0.2f.png'%(start_date,ma,ratio))


#start_date=20130530
#start_date=20160104
#start_date=20100211
#for ma in [3,5,10,15,20,30]:
#    for ratio in [0.01,0.02,0.05,0.01]:
#        get_fig()
#        print ma,ratio
#start_date=20160104

ma=3
ratio=0.01
get_fig()




