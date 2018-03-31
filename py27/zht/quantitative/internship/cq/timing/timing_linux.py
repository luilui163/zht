# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 13:24:50 2016

@author: Administrator
"""

import pandas as pd
import os
import time
import numpy as np

input_dir=''
output_dir=''

def get_paths(path):
    year_names=os.listdir(path)
    year_paths=[os.path.join(path,name) for name in year_names]
    month_paths=[]
    day_paths=[]
    for year_path in year_paths:
        month_names=os.listdir(year_path)
        for month_name in month_names:
            month_paths.append(os.path.join(year_path,month_name))
    for month_path in month_paths:
        day_names=os.listdir(month_path)
        for day_name in day_names:
            day_paths.append(os.path.join(month_path,day_name))
    day_paths=sorted(day_paths,key=lambda day_path:day_path[-8:])
    return day_paths
    
def get_closeprice_df_and_cap_df_of_someday(n):
    global input_dir
    day_paths=get_paths(input_dir)
    raw_lines=open(day_paths[n]).read().split('\n')
    lines=[]
    for l in range(len(raw_lines)):
        if len(raw_lines[l])!=0:#####挑选出A股
            if  raw_lines[l].split(',')[3][0]=='6' or raw_lines[l].split(',')[3][0]=='0' or raw_lines[l].split(',')[3][0]=='3':
                lines.append(raw_lines[l])

    stock_names=[line.split(',')[3] for line in lines]
    closeprice=[float(line.split(',')[5]) for line in lines]
    sector=[line.split(',')[17] for line in lines]
    industry=[line.split(',')[19] for line in lines]
    subindustry=[line.split(',')[20] for line in lines]
    cap=[float(line.split(',')[5])*float(line.split(',')[12]) for line in lines]
    
    closeprice_df=pd.DataFrame({day_paths[n][-8:]:closeprice},index=stock_names)
    sector_df=pd.DataFrame({day_paths[n][-8:]:sector},index=stock_names)
    industry_df=pd.DataFrame({day_paths[n][-8:]:industry},index=stock_names)
    subindustry_df=pd.DataFrame({day_paths[n][-8:]:subindustry},index=stock_names)
    cap_df=pd.DataFrame({day_paths[n][-8:]:cap},index=stock_names)
    
    return (closeprice_df,cap_df,sector_df,industry_df,subindustry_df)



def get_return_df(n):
    (closeprice_df0,cap_df0,sector_df0,industry_df0,subindustry_df0)=get_closeprice_df_and_cap_df_of_someday(n-1)
    (closeprice_df1,cap_df1,sector_df1,industry_df1,subindustry_df1)=get_closeprice_df_and_cap_df_of_someday(n)
    df=pd.concat([closeprice_df0,closeprice_df1],axis=1)
    df=df.dropna(how='any')
    stocks=[k for k in df.index]
    returns=[0]*len(df)
    for i in range(len(df)):
        returns[i]=(df.iat[i,1]-df.iat[i,0])/df.iat[i,0]
    
    return_df=pd.DataFrame({'%d'%n:returns},index=stocks)
    return_df.dropna(how='any')
    return return_df

def get_corr(n):
    return_df0=get_return_df(n-1)
    return_df1=get_return_df(n)
    corr_df=pd.concat([return_df0,return_df1],axis=1)
    corr_df.dropna(how='any')
    corr=corr_df.corr().iat[0,1]
    return corr

def get_Wreturn(n):
    (closeprice_df,cap_df,sector_df,industry_df,subindustry_df)=get_closeprice_df_and_cap_df_of_someday(n)
    return_df=get_return_df(n)
    tmp_df=pd.concat([return_df,cap_df],axis=1)
    tmp_df=tmp_df.dropna(how='any')
    Wreturn=np.average(list(tmp_df.iloc[:,0]),weights=list(tmp_df.iloc[:,1]))
    return Wreturn


def get_snapshot(n):
    (closeprice_df,cap_df,sector_df,industry_df,subindustry_df)=get_closeprice_df_and_cap_df_of_someday(n)
    return_df=get_return_df(n)
    return_df.columns=['returns']
    cap_df.columns=['cap']
    sector_df.columns=['sector']
    industry_df.columns=['industry']
    subindustry_df.columns=['subindustry']
    snapshot=pd.concat([return_df,cap_df,sector_df,industry_df,subindustry_df],axis=1)
    snapshot=snapshot.dropna(how='any')
    return snapshot

def output_timing_files(n,date):
    global output_dir
    snapshot=get_snapshot(n)
    ff=open(os.path.join(output_dir,date+'.txt'),'w')
#    ff=open(r'C:\garbage\%s.txt'%date,'w')
    snapshot[snapshot['returns']>=0.11]=None
    snapshot[snapshot['returns']<=-0.11]=None
    snapshot=snapshot.dropna()
    
    positive=0
    negative=0
    hardenP=0
    hardenN=0
    for i in range(len(snapshot)):
        if snapshot.returns[i]>0:
            positive+=1
        if snapshot.returns[i]>=0.095:
            hardenP+=1
        if snapshot.returns[i]<0:
            negative+=1
        if snapshot.returns[i]<=-0.095:
            hardenN+=1
    hardenDiff=float(hardenP-hardenN)/(len(snapshot))
    ratioDiff=float(positive-negative)/(len(snapshot))

    sector_temp=snapshot.groupby('sector').sum()
    sectorP=0
    sectorN=0
    for j in range(len(sector_temp)):
        if sector_temp.returns[j]>0:
            sectorP+=1
        if sector_temp.returns[j]<=0:
            sectorN+=1
    sectorRatio=float(sectorP-sectorN)/len(sector_temp)          
    
    industry_temp=snapshot.groupby('industry').sum()
    industryP=0
    industryN=0
    for j in range(len(industry_temp)):
        if industry_temp.returns[j]>0:
            industryP+=1
        if industry_temp.returns[j]<=0:
            industryN+=1
    industryRatio=float(industryP-industryN)/len(industry_temp)        
    
    subindustry_temp=snapshot.groupby('subindustry').sum()
    subindustryP=0
    subindustryN=0
    for j in range(len(subindustry_temp)):
        if subindustry_temp.returns[j]>0:
            subindustryP+=1
        if subindustry_temp.returns[j]<=0:
            subindustryN+=1
    subindustryRatio=float(subindustryP-subindustryN)/len(subindustry_temp)
    
    describe=snapshot.describe()
    Mreturn=describe.returns[1]
    std=describe.returns[2]
    median=describe.returns[5]
    skew=snapshot.skew()[0]
    kurt=snapshot.kurt()[0]
    
    corr=get_corr(n)
    Wreturn=get_Wreturn(n)
    
    ff.write('%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f'%(Mreturn,Wreturn,corr,hardenDiff,ratioDiff,sectorRatio,industryRatio,subindustryRatio,median,std,skew,kurt))
    ff.close()





def daily_produce(file_dir,timing_dir):
    global input_dir
    global output_dir
    input_dir=file_dir
    output_dir=timing_dir
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    date=time.strftime("%Y%m%d",time.localtime(time.time()))
    day_paths=get_paths(input_dir)
    dates=[p[-8:] for p in day_paths]
    try:
        n=dates.index(date)
        output_timing_files(n,date)
        print date
    except ValueError:
        pass





if __name__=='__main__':
    daily_produce(file_dir=r'/dat/cqdata/marketdata/bloomberg',timing_dir=r'/dat/datadev/workspace/timing_bloomberg')
    














