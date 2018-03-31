# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 16:12:09 2016

@author: hp
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import util

return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
exchange_rate_diff=pd.read_csv(r'C:\cq\beta_exposure\exchange_rate_diff.csv',index_col=0)
return_df_dates=list(return_df.index)
return_df_stocks=list(return_df.columns)



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

def get_basket(window,stock_number):
    basket_low=[]
    basket_high=[]
    basket_m=[]
    dates=list(exchange_rate_diff.index)
    for d in range(window,len(dates)):
        end_date=dates[d]
        start_date=dates[d-window]
        end_ind=return_df_dates.index(end_date)
        start_ind=return_df_dates.index(start_date)
        
        e=exchange_rate_diff.iloc[d-window:d]
        tmp_df=return_df.iloc[start_ind:end_ind].copy()
        tmp_df['e']=e
        tmp_df[tmp_df==0]=np.nan
        m=tmp_df.dropna(axis=1,thresh=int(window*0.8))
        corr=m.corr().iloc[-1][:-1]
        corr.sort()
        
        tmp_corr=corr.copy()
        m_corr=abs(tmp_corr)
        m_corr.sort()
        
        for i in range(stock_number):
            basket_low.append((end_date,corr.index[i],corr.values[i]))
            basket_high.append((end_date,corr.index[-(i+1)],corr.values[-(i+1)]))
            basket_m.append((end_date,m_corr.index[i],m_corr.values[i]))
        print dates[d]
    return basket_high,basket_low,basket_m

#############################################################################
def get_result(alpha,fig_name):
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
    
    
    month=[y/100 for y in list(cum_sum.index)]
    xticks=[]
    xticklabels=[]
    for i in range(1,len(month)):
        if month[i]>month[i-1]:
            xticks.append(i)
            xticklabels.append(str(month[i]))    

#    year=[y/10000 for y in list(cum_sum.index)]
#    xticks=[]
#    xticklabels=[]
#    for i in range(1,len(year)):
#        if year[i]>year[i-1]:
#            xticks.append(i)
#            xticklabels.append(str(year[i]))
            
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels,rotation=30,fontsize='small')
    ax.set_title('IR=%f'%information_ratio)
    fig.savefig(r'C:\cq\beta_exposure\exchange_rate\combine\%s.png'%fig_name)



#for window in [30,40,50,60]:
#    for stock_number in [3,5,10]:
#        basket_high,basket_low,basket_m=get_basket(window,stock_number)
#        for n,basket in enumerate((basket_high,basket_low,basket_m)):
#            basket_name=['high','low','m']
#            fig_name=basket_name[n]+'_'+str(window)+'_'+str(stock_number)
#            alpha=[]
#            for b in basket:
#                start_date=shift_date(b[0])
#                end_date=start_date
#                alpha.append((b[1],start_date,end_date,1))
#            get_result(alpha,fig_name)
#            print window,stock_number,basket_name[n]


window=30
for stock_number in [10]:
    basket_high,basket_low,basket_m=get_basket(window,stock_number)
    alpha=[]
    for bl in basket_low:
        start_date=shift_date(bl[0])
        end_date=start_date
        alpha.append((bl[1],start_date,end_date,-1))
    for bm in basket_m:
        start_date=shift_date(bm[0])
        end_date=start_date
        alpha.append((bm[1],start_date,end_date,1))
    get_result(alpha,str(window)+'_'+str(stock_number)+'contrast')
    print window,stock_number





#import os
#if not os.path.isdir(r'C:\cq\beta_exposure\exchange_rate\combine\alpha'):
#    os.makedirs(r'C:\cq\beta_exposure\exchange_rate\combine\alpha')
#
#for a in alpha:
#    if os.path.isfile(r'C:\cq\beta_exposure\exchange_rate\combine\alpha\alpha.%d'%a[1]):
#        with open(r'C:\cq\beta_exposure\exchange_rate\combine\alpha\alpha.%d'%a[1],'a') as f:
#            f.write('%s|%f\n'%(a[0],a[3]*1000000))
#    else:
#        with open(r'C:\cq\beta_exposure\exchange_rate\combine\alpha\alpha.%d'%a[1],'w') as f:
#            f.write('%s|%d\n'%(a[0],a[3]*1000000))






