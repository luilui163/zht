#-*-coding: utf-8 -*-
#@author:tyhj
import os
import calendar
import pandas as pd


def mark(func):
    def wrapped():
        func()
        print func.__name__,'finished'
    return wrapped

def _handle_outliers(df):
    new_df=pd.DataFrame(index=df.index)
    for code in df.columns:
        data=df[code]
        data[data-data.mean()<-3*data.std()]=data.mean()-3*data.std()
        data[data-data.mean()>3*data.std()]=data.mean()+3*data.std()
        new_df[code]=data
    return df

def _get_cap_weighted_avg(df,date):
    df=_handle_outliers(df)
    filename=date+'.csv'
    path=r'C:\data\barra_factors\market_value'
    filenames=os.listdir(path)
    if filename in filenames:
        combined_df=pd.DataFrame()
        cap=pd.read_csv(os.path.join(path,filename),index_col=0)
        combined_df['cap']=cap.iloc[:,0]
        combined_df['factor']=df.iloc[:,0]
        combined_df=combined_df.dropna(axis=0,how='any')
        weighted_avg=(combined_df['cap']*combined_df['factor']).sum()*1.0/combined_df['cap'].sum()
        return weighted_avg
    else:
        return 0

def normalize(df,date):
    cap_weighted_avg=_get_cap_weighted_avg(df,date)
    df=(df-cap_weighted_avg)/df.std()

    df=(df-df.mean())/df.std() #TODO:factors are standardized again in barra USE4 empirical notes(page 15)

    return df










