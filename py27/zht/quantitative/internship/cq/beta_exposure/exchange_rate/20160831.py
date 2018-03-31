# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 16:12:09 2016

@author: hp
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from util import *

return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
exchange_rate_diff=pd.read_csv(r'C:\cq\beta_exposure\exchange_rate_diff.csv',index_col=0)
return_df_dates=list(return_df.index)
return_df_stocks=list(return_df.columns)




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


window=30
for stock_number in [5,10,20,30]:
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
        
    position=alpha_to_position(alpha)
    pnl=position_to_pnl(position)
    alpha_folder_name='%d_%d'%(window,stock_number)
    position_to_alpha_file2(position,alpha_folder_name)
    figname=r'20160831\%d_%d.png'%(window,stock_number)
    plot1(pnl,figname)
    print window,stock_number









