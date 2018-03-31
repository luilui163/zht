# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 13:24:50 2016

@author: Administrator
"""

'''
#################################################################################################################################
由于bloomberg数据中对于停牌的额数据，会直接使用上一个工作日的数据，导致return_df中
对应的returns为0，在做portfolio时注意要识别出这些数据
#################################################################################################################################
'''
import re
import pandas as pd
import os

input_dir=''
output_dir=''

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

def get_closeprice_list_and_stock_name_list():
    global input_dir
    day_paths=get_paths(input_dir)
    closeprice_list=[]
    stock_name_list=[]
    dates=[p[-8:] for p in day_paths]
    for i in range(len(day_paths)):
        path=day_paths[i]
        content=open(path).read().split('\n')[:-1]
        lines=[]
        for j in range(len(content)):
            l=content[j]
            try:
                if (l.split(',')[3][0]=='0' or l.split(',')[3][0]=='3' or l.split(',')[3][0]=='6'):
                    lines.append(l)
            except:
                pass
        stock_name=[line.split(',')[3] for line in lines]
        closeprice=[float(line.split(',')[5]) for line in lines]
        stock_name_list.append(stock_name)
        closeprice_list.append(closeprice)
    return closeprice_list,stock_name_list,dates

def get_closeprice_df():
    '''
    注意concat出现下面的错误时可能是因为数据新并入的dataframe中index有重复项
    ValueError: Shape of passed values is (2, 2548), indices imply (2, 2547)
    '''
    closeprice_list,stock_name_list,dates=get_closeprice_list_and_stock_name_list()
    i=0
    df0=pd.DataFrame(closeprice_list[i],index=stock_name_list[i],columns=[dates[i]])
    for i in range(1,len(stock_name_list)):
        df1=pd.DataFrame(closeprice_list[i],index=stock_name_list[i],columns=[dates[i]])
        df=pd.concat([df0,df1],axis=1)
        df0=df
        print i,dates[i]
#    df.T.to_csv()
    return df.T

def get_return_df():
    global output_dir
#    df=pd.read_csv(r'c:\garbage\df.csv',index_col=0)
    df=get_closeprice_df()
    return_df=(df-df.shift(1))/df.shift(1)
    adjusted_return_df=return_df[abs(return_df)<0.11]
    adjusted_return_df.to_csv(output_dir)


if __name__=='__main__':
    input_dir=r'C:\cq\bloomberg'
    output_dir=r'c:\cq\return_df.csv'
    get_return_df()

    




    