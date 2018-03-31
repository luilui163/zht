# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 09:57:26 2016

@author: hp
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

announcement_date_df=pd.read_csv(r'c:\cq\announcement_date.csv',index_col=0)
return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
return_df_stocks=list(return_df.columns)
return_df_dates=list(return_df.index)

def shift_date(d,shift_num=1):
    d=int(d)
    if shift_num>0:
        if d<return_df_dates[0]:
            print d,'out of return_df_date\'s range'
        elif d>return_df_dates[-shift_num-1]:
            return return_df_dates[-1]
        elif d in return_df_dates:
            ind=return_df_dates.index(d)
            return return_df_dates[ind+shift_num]
        else:
            for i in range(len(return_df_dates)):
                if return_df_dates[i]<d and return_df_dates[i+1]>d:
                    return return_df_dates[i+shift_num]
    elif shift_num==0:
        if d<return_df_dates[0]:
            print d,'is too small'
        elif d>return_df_dates[-1]:
            print d,'is too large'
        elif d in return_df_dates:
            return d
        else:
            for i in range(len(return_df_dates)):
                if return_df_dates[i]<d<return_df_dates[i+1]:
                    return return_df_dates[i+1]
    elif shift_num<0:
        num=-shift_num
        if d<return_df_dates[num-1]:
            print d,'is too small'
        elif d>return_df_dates[-1]:
            print d,'is too large'
        elif d in return_df_dates:
            ind=return_df_dates.index(d)
            return return_df_dates[ind-num]
        else:
            for i in range(len(return_df_dates)):
#                if return_df_dates[i]<=d and return_df_dates[i+1]>d:
                if return_df_dates[i]<d<return_df_dates[i+1]:
                    return return_df_dates[i+1-num]
    
'''                
#strategy1 持股增多时，long，减少时short，不考虑数量相同，但是股票变化的情况
'''
def get_basket1():
    file_dir=r'C:\cq\share_holding\data'
    file_name=os.listdir(file_dir)
    file_path=[os.path.join(file_dir,fn) for fn in file_name]
    basket=[]
    for fp in file_path:
        lines=open(fp).read().split('\n')[:-1]
        for i in range(1,len(lines)):
            stocks1=lines[i-1].split('|')[-1].split('\t')
            stocks2=lines[i].split('|')[-1].split('\t')
            if len(stocks2)>len(stocks1):
                basket.append((fp.split('\\')[-1],lines[i].split('|')[0],1))
            elif len(stocks2)<len(stocks1):
                basket.append((fp.split('\\')[-1],lines[i].split('|')[0],-1))
    return basket
'''
#strategy2 新持有的股票上个季度的收益情况，对本股票的影响,在选股时候，会有一个threshold，如果alpha收益
大于threshold就long，深入一点，还要考虑到对股票的持有量，来计算最后的alpha return
'''
def get_the_quarter_returns_of_one_stock(sid,end_date):
    end_date=int(end_date)
    q_dates=list(announcement_date_df.index)
    start_date=q_dates[q_dates.index(end_date)-1]
    market_return=return_df.mean(axis=1)
#    start_date=shift_date(start_date,0)
#    end_date=shift_date(end_date,0)
    tmp_df=return_df[sid].loc[start_date:end_date]-market_return.loc[start_date:end_date]
    return tmp_df.sum()
    
def get_alpha_returns():
    file_dir=r'C:\cq\share_holding\data'
    file_name=os.listdir(file_dir)
    file_path=[os.path.join(file_dir,fn) for fn in file_name]
    alpha_returns=[]
    for n,fp in enumerate(file_path):
#        fp=file_path[0]
        lines=open(fp).read().split('\n')[:-1]
        for i in range(1,len(lines)):
            date=lines[i].split('|')[0]
            stocks1=lines[i-1].split('|')[-1].split('\t')
            stocks2=lines[i].split('|')[-1].split('\t')
            new_stock=[s for s in stocks2 if s not in stocks1]
            new_stock=[ns for ns in new_stock if ns  in return_df_stocks]
            if new_stock!=[]:
                sum_alpha_returns=0
                for ns in new_stock:
                    sum_alpha_returns+=get_the_quarter_returns_of_one_stock(ns,lines[i].split('|')[0])
                alpha_returns.append((fp.split('\\')[-1],date,sum_alpha_returns))
        print n,fp
    return alpha_returns

def get_basket2(threshold):
    alpha_returns=get_alpha_returns()
    basket=[]
    for a in alpha_returns:
        basket.append((a[0],a[1],-1))
#        if a[2]>threshold:
#            basket.append((a[0],a[1],1))
#        if a[2]<-threshold:
#            basket.append((a[0],a[1],-1))
    return basket
'''
strategy3:

'''




for threshold in [0]:
    basket=get_basket2(alpha_returns,threshold)
    
    for length in [1,2,3,5,10,30,50,80]:
        alpha=[]
        for s in basket:
            start_date=shift_date(int(s[1]))
            end_date=shift_date(start_date,length)
            alpha.append((s[0],start_date,end_date,s[2]))
        
        
        position_df=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
        position_df[position_df==0]=np.nan
        
        col=list(return_df.columns)
        for n,a in enumerate(alpha):
            col_index=col.index(a[0])
            if a[1] and a[2]:
                start_index=return_df_dates.index(int(a[1]))
                end_index=return_df_dates.index(int(a[2]))
                #deal with limit before the day to invest
                if abs(return_df.iat[start_index-1,col_index])<0.095:
                    for i in range(start_index,end_index+1):
                        position_df.iat[i,col_index]=a[3]
        
        #adjust position
        expose_position=pd.Series([np.nan]*len(return_df.index),index=return_df.index)
        for i in range(len(return_df.index)):
            row=position_df.iloc[i]
            long_position=row[row>0].sum()
            short_position=abs(row[row<0].sum())
            if long_position or short_position:
                if long_position>short_position:
                    row[row>0]=row[row>0]/(2*long_position)
                    row[row<0]=row[row<0]/(2*long_position)
                    expose_position.values[i]=-(long_position-short_position)/(2*long_position)
                elif long_position==short_position:
                    row[row>0]=row[row>0]/(2*long_position)
                    row[row<0]=row[row<0]/(2*long_position)
                    expose_position.values[i]=0.0
                else:
                    row[row>0]=row[row>0]/(2*short_position)
                    row[row<0]=row[row<0]/(2*short_position)
                    expose_position.values[i]=(short_position-long_position)/(2*short_position)
                
        #deal with stock splitting
        hold_df=return_df.copy()
        hold_df[abs(hold_df)>0.15]=0
        
        #deal with limit after signal
        hold_df[abs(hold_df)>0.095]=0
        
        #caculate the stock pnl
        market_return=return_df.mean(axis=1)
        stock_pnl_df=hold_df*position_df
        stock_pnl=stock_pnl_df.sum(axis=1)
        pnl=stock_pnl+expose_position*market_return
        for e,k in enumerate(pnl):
            if pd.notnull(k):
                break
    
        pnl=pnl[e:]
        pnl.values[0]=0
        pnl=pnl.fillna(0)
        std=pnl.std()
        avg=pnl.mean()
        cum_sum=pnl.cumsum()
        information_ratio=avg/std
        fig=plt.figure()
        ax=fig.add_subplot(1,1,1)
        ax.plot(cum_sum)
    
        year=[y/10000 for y in list(cum_sum.index)]
        xticks=[]
        xticklabels=[]
        for i in range(1,len(year)):
            if year[i]>year[i-1]:
                xticks.append(i)
                xticklabels.append(str(year[i]))
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels,rotation=30,fontsize='small')
        ax.set_title('IR=%f'%information_ratio)
        fig.savefig(r'C:\cq\share_holding\fig\no_threshold\{threshold}_{length}.png'.format(threshold=threshold,length=length))
        print threshold,length
        
    
    
    



















