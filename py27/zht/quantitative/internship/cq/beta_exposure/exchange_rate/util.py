
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 15:11:57 2016

@author: hp
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os
import datetime


return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
return_df_stocks=list(return_df.columns)
return_df_dates=list(return_df.index)

def normalize_date(date):
    '''
    normalize date with form in '2016-03-09' or '2012/3/6'
    '''
    try:
        int(date)
        return date
    except:
        if '-' in date:
            year,month,day=tuple(date.split('-'))
        elif r'/' in date:
            year,month,day=tuple(date.split(r'/'))
            
        if len(month)==1:
            month='0'+month
        if len(day)==1:
            day='0'+day
        return year+month+day
    
def normalize_sid(sid):
    sid=sid.upper()
    sid=sid.replace('SH','SS')
    if sid in return_df_stocks:
        return sid
    else:
        return None

def shift_date(d,shift_num=2):
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

def alpha_to_position(alpha):
    position_df=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    position_df[position_df==0]=np.nan
    for a in alpha:
        start_date=int(a[1])
        end_date=int(a[2])
        position_df.loc[start_date:end_date,a[0]]=a[3]
        
    #deal with stock splitting and dividend
    valid_return_df=return_df.copy()
    valid_return_df[abs(valid_return_df)>0.11]=np.nan
    
    #deal with limit after signal
    valid_return_df[abs(valid_return_df)>0.095]=np.nan
    
    #deal with limit before signal
    p=position_df.copy()
    p[p>0]=1
    p[p<0]=-1
    valid_return_df[valid_return_df.shift()*p>0.95]=np.nan
#    valid_return_df[valid_return_df.shift()>0.095]=np.nan    
    '''
    something need to improve:we should just remove those 涨停 stock if we long some stocks,if we long 
    then ,we just need to remove 跌停.
    '''
    
    #adjust position,delete those stocks not in exchange
    position_df[pd.isnull(valid_return_df)]=np.nan
    
    #adjust the position to let their long position and short position's sum equal to 1 and -1
    for i in range(len(return_df.index)):
        row=position_df.iloc[i]
        long_position=row[row>0].sum()
        short_position=abs(row[row<0].sum())
        row[row>0]/=2.0*long_position
        row[row<0]/=2.0*short_position
        '''
        notice that the change in row will be synchronized in position_df if pd.copy not used
        '''
    return position_df

def position_to_pnl(position_df):
    #calculate expose_position
    market_hedge_position=pd.Series([np.nan]*len(return_df.index),index=return_df.index)
    for i in range(len(return_df.index)):
        row=position_df.iloc[i]
        sum_position=row.sum()
        if sum_position>0:
            market_hedge_position.values[i]=-0.5
        elif sum_position<0:
            market_hedge_position.values[i]=0.5
    #caculate the stock pnl
    adjust_return_df=return_df.copy()
    #split or dividend stock should be removed before calculate the market returns
    adjust_return_df[abs(adjust_return_df)>0.11]=np.nan
    market_return=adjust_return_df.mean(axis=1)
    
    #since those invalid returns has been removed in position_df by set 
    #those data as np.nan in last but one line of function 'alpha_to_position',
    #so,in this place,we can just multi return_df with position_df
    stock_pnl_df=return_df*position_df
    stock_pnl=stock_pnl_df.sum(axis=1)
    pnl=stock_pnl+market_hedge_position*market_return
    
    return pnl


#def position_to_pnl(position_df):
#    #deal with stock splitting and dividend
#    valid_return_df=return_df.copy()
#    valid_return_df[abs(valid_return_df)>0.11]=np.nan
#    
#    #deal with limit after signal
#    valid_return_df[abs(valid_return_df)>0.095]=np.nan
#    
#    #deal with limit before signal
#    valid_return_df[valid_return_df.shift()>0.095]=np.nan    
#    '''
#    something need to improve:we should just remove those 涨停 stock if we long some stocks,if we long 
#    then ,we just need to remove 跌停.
#    '''
#    
#    #adjust position
#    position_df[pd.isnull(valid_return_df)]=np.nan
#
#    #calculate expose_position
#    expose_position=pd.Series([np.nan]*len(return_df.index),index=return_df.index)
#    for i in range(len(return_df.index)):
#        row=position_df.iloc[i]
#        long_position=row[row>0].sum()
#        short_position=abs(row[row<0].sum())
#        if long_position>0 and short_position>0:
#            row[row>0]=row[row>0]/(2*long_position)
#            row[row<0]=row[row<0]/(2*short_position)
#            expose_position.values[i]=0.0
#        elif short_position>0:
#            expose_position.values[i]=0.5
#        elif long_position>0:
#            expose_position.values[i]=-0.5
#            
#    #caculate the stock pnl
#    adjust_return_df=return_df.copy()
#    #split or dividend stock should be removed before calculate the market returns
#    adjust_return_df[abs(adjust_return_df)>0.11]=np.nan
#    market_return=adjust_return_df.mean(axis=1)
#    stock_pnl_df=valid_return_df*position_df
#    stock_pnl=stock_pnl_df.sum(axis=1)
#    pnl=stock_pnl+expose_position*market_return
#    
#    return pnl



def plot1(pnl,figname=None):
    for e,k in enumerate(pnl):
        if pd.notnull(k):
            break
    pnl=pnl[e-1:]
#    pnl=pnl[e:]
#    pnl.values[0]=0#why?
    std=pnl.std()
    avg=pnl.mean()
    information_ratio=avg/std
    pnl=pnl.fillna(0)
    cum_sum=pnl.cumsum()
    fig,ax=plt.subplots(1,1,figsize=(12,8))
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
    if figname:
        fig.savefig(figname)

def plot2(variable):
    if variable.datatype=='c':
        categorys=continuous_category(variable)
    elif variable.datatype=='d':
        categorys=discrete_category(variable)
    pnls={}
    for category in categorys:
        pnls[category.id]=category.pnl
    
    pnl_df=pd.DataFrame(pnls)
    
    e=0
    for i in range(len(pnl_df)):
        flag=0
        for j in range(len(pnl_df.columns)):
            if pd.notnull(pnl_df.iat[i,j]):
                flag=1
                break
        if flag:
            e=i
            break
        
    pnl_df=pnl_df.iloc[e:]
    count=pnl_df[pd.notnull(pnl_df)].count()
    positive=pnl_df[pnl_df>0].count()
    win_rate=positive/count
    
    #information ratio
    pnl_df.iloc[0]=0
    std=pnl_df.std()
    avg=pnl_df.mean()
    information_ratio=avg/std
    
    #win_rate
    count=pnl_df[pd.notnull(pnl_df)].count()
    positive=pnl_df[pnl_df>0].count()
    win_rate=positive/count
    
    pnl_df=pnl_df.fillna(0)
    cum_sum=pnl_df.cumsum()
    fig,ax=plt.subplots(1,1,figsize=(12,8))
    #fig=plt.figure()
    #ax=fig.add_subplot(1,1,1)
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

    plt.legend(tuple(pnl_df.columns),loc='upper left')
    plt.title(variable.name)
    
    if not os.path.isdir('observe_variable'):
        os.makedirs('observe_variable')
    
    figname=r'observe_variable\%s.png'%variable.name
    fig.savefig(figname)
    
    description=[(categorys[i].id,categorys[i].name,information_ratio[i],win_rate[i]) for i in range(len(categorys))]
    description.sort(key=lambda x:x[2],reverse=True)
    
    with open('observe_variable\%s_description.txt'%variable.name,'w') as f:
        for des in description:
            f.write('%d\t%s\t%f\t%f\n'%des)


def position_to_alpha_file1(position,folder='alpha'):
    '''
    周一读前面 周五 周六周日的数据，周二到周五读前面一天的数据。
    其实应该读上一个工作日之后的数据
    '''
    if not os.path.isdir(folder):
        os.makedirs(folder)
    
    e=0
    for i in range(len(position)):
        for j in range(len(position.columns)):
            if pd.notnull(position.iat[i,j]):
                e=i
                break
        if e>0:
            break
        
    for i in range(e,len(position)):
        date=position.index[i]
        row=position.iloc[i,:]
        date_date=datetime.datetime.strptime(str(date),'%Y%m%d')
        week_date=date_date.weekday()
        if week_date<=1:
            alpha_date=date_date-datetime.timedelta(days=4)#weekday
        elif 1<week_date<=6:
            alpha_date=date_date-datetime.timedelta(days=2)# the parameter is days=2,because the date_date is T+1
            
        alpha_date_str=datetime.datetime.strftime(alpha_date,'%Y%m%d')
        
        with open(r'%s\alpha.%s'%(folder,alpha_date_str),'w') as f:
            for j in range(len(row)):
                if pd.notnull(row[j]):
                    stock=position.columns[j]
                    p=row[j]*20000000
                    f.write('%s|%f\n'%(stock,p))
        print 'position_to_alpha',date


def position_to_alpha_file2(position,folder='alpha'):
    '''
    周一读前面 周五 周六周日的数据，周二到周五读前面一天的数据。
    其实应该读上一个工作日之后的数据
    '''
    if not os.path.isdir(folder):
        os.makedirs(folder)
        
    e=0
    for i in range(len(position)):
        for j in range(len(position.columns)):
            if pd.notnull(position.iat[i,j]):
                e=i
                break
        if e>0:
            break
        
    for i in range(e,len(position)):
        date=position.index[i]
        row=position.iloc[i,:]
        date_date=datetime.datetime.strptime(str(date),'%Y%m%d')
        week_date=date_date.weekday()
        if week_date<=1:
            alpha_date=date_date-datetime.timedelta(days=4)#weekday
        elif 1<week_date<=6:
            alpha_date=date_date-datetime.timedelta(days=2)# the parameter is days=2,because the date_date is T+1
            
        alpha_date_str=datetime.datetime.strftime(alpha_date,'%Y%m%d')
        
        #adjust the weight to ensure the sum is 1.
        #================================================================
        row=row/abs(row.sum())
        #================================================================
        with open(r'%s\alpha.%s'%(folder,alpha_date_str),'w') as f:
            for j in range(len(row)):
                if pd.notnull(row[j]):
                    stock=position.columns[j]
                    '''
                    notice the value to multiply
                    '''
                    p=row[j]*10000000
                    f.write('%s|%f\n'%(stock,p))
        print 'position_to_alpha',date


def get_plain_weight(data,delay_day=2,length=1):
    weight=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    weight[weight==0]=np.nan
    for n,d in enumerate(data):
        try:
            stock=d[0]
            date=d[1]
            start_date=shift_date(date,delay_day)
            end_date=shift_date(start_date,length-1)
            weight.loc[start_date:end_date,stock]=-1
            '''
            notice that loc slice is different from iloc:
            for example:
            
                return_df.loc[20041105:20041108,'603998.SS':'603999.SS']
                it will  include 20041108 and '603999.SS'
                
                return_df.iloc[0:1,0:4]
                it won't include index 1 and column 4
            '''
        except:
            pass
        print n
    return weight