# -*- coding: utf-8 -*-
"""
term,industry,underwriter,credit rating,issuing scale/market value
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
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
    

    year=[y/10000 for y in list(cum_sum.index)]
    xticks=[]
    xticklabels=[]
    for i in range(1,len(year)):
        if year[i]>year[i-1]:
            xticks.append(i)
            xticklabels.append(str(year[i]))
            
#    month=[y/100 for y in list(cum_sum.index)]
#    xticks=[]
#    xticklabels=[]
#    for i in range(1,len(month)):
#        if month[i]>month[i-1]:
#            xticks.append(i)
#            xticklabels.append(str(month[i]))    

    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels,rotation=30,fontsize='small')
    ax.set_title('IR=%f'%information_ratio)
    fig.savefig(fig_name)



def get_alpha(length,term_thresh=0,credit_rank='AAA'):
    path=r'C:\cq\convertible_bond\data1.txt'
    lines=open(path).read().split('\n')[1:-1]
    alpha=[]
    for l in lines:
        sid=l.split('\t')[6]
#        issuing_scale=l.split('\t')[1]
#        term=l.split('\t')[2]
        credit_rating=l.split('\t')[3]
        issuing_announcement_date=l.split('\t')[4]
#        listed_date=l.split('\t')[5]

        start_date=shift_date(issuing_announcement_date,1)
        end_date=shift_date(start_date,length)
        if credit_rating==credit_rank:
            alpha.append((sid,start_date,end_date,1))
            print issuing_announcement_date
    return alpha

for length in [1,2,5,10,30,50]:
    for credit_rank in ['AA','AAA']:
        alpha=get_alpha(length,term_thresh)
        figname=r'C:\cq\convertible_bond\issuing_announcement_date_with_credit_rating_AAA\%d_%s.png'%(length,credit_rank)
        get_result(alpha,figname)
        print length