# -*- coding: utf-8 -*-
"""
Created on Fri Aug 05 14:20:45 2016

@author: hp
"""
import xlrd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
return_df_dates=list(return_df.index)
return_df_stocks=list(return_df.columns)

def shift_date(d,shift_num=1):
    d=int(d)
    if d<return_df_dates[0]:
        print d,'out of return_df_date\'s range'
    elif d>return_df_dates[-shift_num-1]:
        return return_df_dates[-1]
    elif d in return_df_dates:
        ind=return_df_dates.index(d)
        return return_df_dates[ind+shift_num]
    else:
        for i in range(len(return_df_dates)):
            if return_df_dates[i]<=d and return_df_dates[i+1]>d:
                return return_df_dates[i+1+shift_num]



def get_items():
    data = xlrd.open_workbook(r'c:\cq\lawsuit\lawsuit_new.xlsx')
    table = data.sheets()[0]
    nrows = table.nrows
    items=[]
    for i in range(2,nrows-1):
        line=table.row_values(i)
        stock_code=line[0]
        stock_name=line[1]
        announcement_date=line[2]
    #    print announcement_date
        suit_name=line[3]
        accuser=line[5]
        accused=line[6]
        suit_type=line[7]
        amount=line[8]
        accuse_date=line[10]
        judgement_date=line[12]
        sue=line[14]
        sue_party=line[15]
        csrc_industry=line[20]
        eastmoney_industry=line[21]
#        l=[stock_code,stock_name,announcement_date,suit_name,accuser,accused,suit_type,amount,accuse_date,judgement_date,sue,sue_party,csrc_industry,eastmoney_industry]
        items.append((stock_code,stock_name,announcement_date,suit_name,accuser,accused,suit_type,amount,accuse_date,judgement_date,sue,sue_party,csrc_industry,eastmoney_industry))
    
    return items

items=get_items()

'''
0 stock_code
1 stock_name
2 announcement_date
3 suit_name
4 accuser
5 accused
6 suit_type
7 amount
8 accuse_date
9 judgement_date
10 sue
11 sue_party
12 csrc_industry
13 eastmoney_industry
'''

def handle_date_format(li):
    return [str(int(l)) for l in li if l>0]
            
announcement_date_df=pd.read_csv(R'c:\cq\announcement_date.csv',index_col=0)
df_stocks=list(announcement_date_df.columns)

in_report=[]
out_report=[]
for item in items:
    if item[0] in df_stocks:
        report_dates=list(announcement_date_df[item[0]])
        if item[2] in handle_date_format(report_dates):
            in_report.append(item)
            print item[0],item[2]
        else:
            out_report.append(item)
            print item[0],item[2]
print len(in_report)



dummy_in_report=[]
for item in in_report:
    if (item[1] not in item[4]) and (item[1] not in item[5]):
        dummy_in_report.append(item)
        
dummy_out_report=[]
for item in out_report:
    if (item[1] not in item[4]) and (item[1] not in item[5]):
        dummy_out_report.append(item)


accuser_out_report=[]
for item in out_report:
    if item[1] in item[4]:
        accuser_out_report.append(item)
        print item[1]

accuser_in_report=[]
for item in in_report:
    if item[1] in item[4]:
        accuser_in_report.append(item)
        
accused_out_report=[]
for item in out_report:
    if item[1] in item[5]:
        accused_out_report.append(item)

accused_in_report=[]
for item in in_report:
    if item[1] in item[5]:
        accused_out_report.append(item)

alpha=[]
for item in accuser_out_report:
    if item[8]!='':
        if item[0] in return_df_stocks:
            if int(str(item[8]))>return_df_dates[0]:
                start_date=shift_date(str(item[8]))
                end_date=start_date
                alpha.append((item[0],start_date,end_date,1))
                print item[0]


def get_result(alpha):
    target_df=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    target_df[target_df==0]=np.nan
    
    for n,na in enumerate(alpha):
        col_index=return_df_stocks.index(na[0])
        start_index=return_df_dates.index(int(na[1]))
        end_index=return_df_dates.index(int(na[2]))
        for i in range(start_index,end_index+1):
            target_df.iat[i,col_index]=na[3]
    
    t=target_df.sum(axis=1)
    r=return_df.mean(axis=1)
    for i in range(len(t)):
        if t.values[i]<0:
            r.values[i]=r.values[i]*(-1)    
    
    #alpha=-1*factor
    pnl=((return_df*target_df).sum(axis=1))/abs(t)-r
    pnl[abs(pnl)>0.09]=0
    
    for e,p in enumerate(pnl):
        if pd.notnull(p):
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
#    fig.savefig(r'C:\cq\lawsuit\fig\accuse_date_accuser_out_report.png')

        
get_result(alpha)
        
        