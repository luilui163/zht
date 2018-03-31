# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 13:24:50 2016

@author: Administrator
"""
import re
import pandas as pd
import os
import time
import datetime
import numpy as np

input_dir=r'c:\cq\bloomberg'
output_dir=r'c:\cq\cap_df.csv'

def get_paths(path):
    p=re.compile('\d{8}\Z')
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
            if bool(re.findall(p,day_name)):
                day_paths.append(os.path.join(month_path,day_name))
    day_paths=sorted(day_paths,key=lambda day_path:day_path[-8:])
    return day_paths
    
def get_cap_df_of_someday(n):
    global input_dir
    day_paths=get_paths(input_dir)
    raw_lines=open(day_paths[n]).read().split('\n')
    lines=[]
    for l in range(len(raw_lines)):
        if len(raw_lines[l])!=0:#####挑选出A股
            if  raw_lines[l].split(',')[3][0]=='6' or raw_lines[l].split(',')[3][0]=='0' or raw_lines[l].split(',')[3][0]=='3':
                lines.append(raw_lines[l])

    stock_names=[line.split(',')[3] for line in lines]
    cap=[float(line.split(',')[5])*float(line.split(',')[12]) for line in lines]
    cap_df=pd.DataFrame({day_paths[n][-8:]:cap},index=stock_names)
    return cap_df

def get_cap_df():
    global input_dir,output_dir
    day_paths=get_paths(input_dir)
    i=0
    df0=get_cap_df_of_someday(0)
    for i in range(1,len(day_paths)):
        df1=get_cap_df_of_someday(i)
        df=pd.concat([df0,df1],axis=1)
        df0=df
        print i,day_paths[i]
    df0.T.to_csv(output_dir)

if __name__=='__main__':
    input_dir=r'c:\cq\bloomberg'
    output_dir=r'c:\cq\cap_df.csv'
    get_cap_df()
    