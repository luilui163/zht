# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 14:51:47 2016

@author: hp
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os


return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
return_df_stocks=list(return_df.columns)
return_df_dates=list(return_df.index)

def change_sid(sid):
    return_df_sid=[r.split('.')[0] for r in return_df_stocks]
    if sid in return_df_sid:
        ind=return_df_sid.index(sid)
        return return_df_stocks[ind]

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


#############################################################################
def alpha_to_position_df(alpha):
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
    return position_df

def get_result(position_df,fig_name):
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
    hold_df[abs(hold_df)>0.11]=0
    
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
    ax.set_title('IR=%f'%information_ratio)
    fig.savefig(fig_name)
#    fig.savefig(r'C:\cq\restricted_share\contrast6\{length}.png'.format(length=length))



def get_alpha(eps_thresh=0.095,start_delay=1,hold_length=1):
    file_dir=r'C:\cq\1\earning'
    file_names=os.listdir(file_dir)
    file_paths=[os.path.join(file_dir,fn) for fn in file_names]
    file_paths.sort(key=lambda x:int(x[-12:-4]))
    alpha=[]
    for fp in file_paths:
        start_date=shift_date(fp[-12:-4],start_delay)
        end_date=shift_date(start_date,hold_length)
        lines=open(fp).read().split('\n')[:-1]
        for l in lines:
            stock=l.split(',')[0]
            eps=l.split(',')[2]
            eps_lastyear=float(l.split(',')[3])
            try:
                revenue_quartergrowth=float(l.split(',')[5])
#                netprofit_quartergrowth=float(l.split(',')[8])
#                bps=float(l.split(',')[9])
#                roe=float(l.split(',')[10])
#                cps=float(l.split(',')[11])
                if stock in return_df_stocks and float(eps)<eps_thresh and -1<eps_lastyear<0.1 and revenue_quartergrowth<0:
                        alpha.append((stock,start_date,end_date,-1))
            except:
                pass
        print fp[-12:-4]
    return alpha

#hold after release

alpha=get_alpha()
position_df=alpha_to_position_df(alpha)
figname=r'C:\cq\1\final.png'
get_result(position_df,figname)



'''
eps_thresh<0.095
0.1>eps_lastyear_thresh>-1
revenue_quartergrowth<0
'''

#hold after n day delay
#hold_length=1
#for start_delay in [200]:
#    alpha=get_alpha(start_delay,hold_length)
#    position_df=alpha_to_position_df(alpha)
#    figname=r'C:\cq\1\hold_after_delay_n_days\%d.png'%start_delay
#    get_result(position_df,figname)
#    print start_delay

#ind=list(target_df.index)
#col=list(target_df.columns)
#for i in range(len(ind)):
#	stocks=[]
#	for j in range(len(col)):
#		if pd.notnull(target_df.iat[i,j]):
#			stocks.append(col[j])
#	if len(stocks)>0:
#		position=10000000.0/len(stocks)
#		with open(r'C:\cq\restricted_share\alpha\alpha.{date}'.format(date=ind[i]),'w') as f:
#			for s in stocks:
#				f.write(s+'|'+str(position)+'\n')
#	print i
				