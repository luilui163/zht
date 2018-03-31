# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 13:24:50 2016

@author: Administrator
"""

import pandas as pd
import os
import time
import numpy as np

start=time.time()

###
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
day_paths=get_paths(r'C:\bloomberg_new\bloomberg')

def get_closeprice_df_and_cap_df_of_someday(day_paths,day_number):
    raw_lines=open(day_paths[day_number]).read().split('\n')
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
    
    closeprice_df=pd.DataFrame({day_paths[day_number][-8:]:closeprice},index=stock_names)
    sector_df=pd.DataFrame({day_paths[day_number][-8:]:sector},index=stock_names)
    industry_df=pd.DataFrame({day_paths[day_number][-8:]:industry},index=stock_names)
    subindustry_df=pd.DataFrame({day_paths[day_number][-8:]:subindustry},index=stock_names)
    cap_df=pd.DataFrame({day_paths[day_number][-8:]:cap},index=stock_names)
    
    return (closeprice_df,cap_df,sector_df,industry_df,subindustry_df)

def get_closeprice_df_and_cap_df(day_paths):
    (closeprice_df,cap_df,sector_df,industry_df,subindustry_df)=get_closeprice_df_and_cap_df_of_someday(day_paths,0)
    for i in range(1,len(day_paths)):
        (closeprice_df_i,cap_df_i,sector_df_i,industry_df_i,subindustry_df_i)=get_closeprice_df_and_cap_df_of_someday(day_paths,i)
        closeprice_df=pd.concat([closeprice_df,closeprice_df_i],axis=1)
        cap_df=pd.concat([cap_df,cap_df_i],axis=1)
        sector_df=pd.concat([sector_df,sector_df_i],axis=1)
        industry_df=pd.concat([industry_df,industry_df_i],axis=1)
        subindustry_df=pd.concat([subindustry_df,subindustry_df_i],axis=1)
    return (closeprice_df,cap_df,sector_df,industry_df,subindustry_df)
(closeprice_df,cap_df,sector_df,industry_df,subindustry_df)=get_closeprice_df_and_cap_df(day_paths)
#closeprice_df.to_csv(r'C:\bloomberg_new\closeprice_df.csv')
#cap_df.to_csv(r'C:\bloomberg_new\cap_df.csv')
#sector_df.to_csv(r'C:\bloomberg_new\sector_df.csv')
#industry_df.to_csv(r'C:\bloomberg_new\industry_df.csv')
#subindustry_df.to_csv(r'C:\bloomberg_new\subindustry_df.csv')
#closeprice_df=pd.read_csv(r'C:\bloomberg_new\closeprice_df.csv',index_col=0).T

def get_return_df(closeprice_df):
    closeprice_df=closeprice_df.T
    date=[d for d in closeprice_df.index][1:]
    i=0
    returns=np.diff(np.array(closeprice_df.iloc[:,i]))/np.array(closeprice_df.iloc[:,i])[:-1]
    return_df=pd.DataFrame({closeprice_df.columns[i]:returns},index=date)
    
    for i in range(1,len(closeprice_df.T)):
        returns=np.diff(np.array(closeprice_df.iloc[:,i]))/np.array(closeprice_df.iloc[:,i])[:-1]
        tmpDF=pd.DataFrame({closeprice_df.columns[i]:returns},index=date)
        return_df=pd.concat([return_df,tmpDF],axis=1)
    return return_df
return_df=get_return_df(closeprice_df)
#return_df.to_csv(r'C:\bloomberg_new\return_df.csv')

#closeprice_df=pd.read_csv(r'C:\bloomberg_new\closeprice_df.csv',index_col=0)
#return_df=pd.read_csv(r'C:\bloomberg_new\return_df.csv',index_col=0)
#cap_df=pd.read_csv(r'c:\bloomberg_new\cap_df.csv',index_col=0)
#sector_df=pd.read_csv(r'c:\bloomberg_new\sector_df.csv',index_col=0)
#industry_df=pd.read_csv(r'c:\bloomberg_new\industry_df.csv',index_col=0)
#subindustry_df=pd.read_csv(r'c:\bloomberg_new\subindustry_df.csv',index_col=0)
cap_df=cap_df.drop('20041105',axis=1)###因为return_df 没有20041105这天的数据
sector_df=sector_df.drop('20041105',axis=1)
industry_df=industry_df.drop('20041105',axis=1)
subindustry_df=subindustry_df.drop('20041105',axis=1)


def get_snapshot_of_someday(n,return_df,cap_df,sector_df,industry_df,subindustry_df):
    snapshot=pd.DataFrame({'returns':return_df.T.iloc[:,n],
                           'cap':cap_df.iloc[:,n],
                            'sector':sector_df.iloc[:,n],
                            'industry':industry_df.iloc[:,n],
                            'subindustry':subindustry_df.iloc[:,n]
                            },index=[s for s in cap_df.index])
    snapshot=snapshot.dropna(how='any')
    return snapshot

def get_corr(return_df):
    corr=[0]*len(return_df)
    for i in range(1,len(return_df)):
        temp1=return_df.T.iloc[:,i]
        temp2=return_df.T.iloc[:,i-1]
        temp=pd.concat([temp1,temp2],axis=1)
        temp.dropna(how='any')
        corr[i]=temp.corr().iat[0,1]
    return corr
corr=get_corr(return_df)

def output_timing_files(return_df,cap_df,sector_df,industry_df,subindustry_df,corr):
    for n in range(1,len(return_df)):
        snapshot=get_snapshot_of_someday(n,return_df,cap_df,sector_df,industry_df,subindustry_df)
        date=str([d for d in return_df.index][n])
        ff=open(r'C:\bloomberg_new\timing/%s.txt'%date,'w')
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
        mean=describe.returns[1]
        std=describe.returns[2]
        median=describe.returns[5]
        skew=snapshot.skew()[1]
        kurt=snapshot.kurt()[1]
        
        weightedReturn=np.average(list(snapshot.returns),weights=list(snapshot.cap))    
        
        ff.write('%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f'%(mean,weightedReturn,corr[n],hardenDiff,ratioDiff,sectorRatio,industryRatio,subindustryRatio,median,std,skew,kurt))
        ff.close()
        print date

output_timing_files(return_df,cap_df,sector_df,industry_df,subindustry_df,corr)


end=time.time()
print end-start






