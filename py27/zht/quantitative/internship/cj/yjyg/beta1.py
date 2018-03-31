#-*-coding: utf-8 -*-
#@author:tyhj
from sklearn import datasets,linear_model
import pandas as pd
import numpy as np
from zht.data import data_handler
from datetime import datetime
import time


length=250
def get_df():
    codes=data_handler.get_code_list()
    hs300=data_handler.get_index_df()

    df=pd.DataFrame()
    for code in codes:
        df[code]=data_handler.get_df(code)['close']
    df['hs300']=hs300['close']
    # prune some stocks which have not enough history data
    df=df.loc[hs300.index[0]:]
    df=df.dropna(axis=1,thresh=length*0.6)
    df.index=[pd.to_datetime(ind) for ind in df.index]
    df=df.pct_change()
    return df

def get_month_end(df):
    start_date=df.index[250]
    end_date=df.index[-1]
    month_ends=pd.date_range(start_date,end_date,freq='M')
    return month_ends

def get_regression_sample(df,month_end):
    #get the latest 'length' days' data
    df_sub=df.truncate(after=month_end)
    df_sub=df_sub[-length:]
    df_sub=df_sub.dropna(axis=1,thresh=length*0.6)
    #get halflife weight
    w = [pow(0.5, i / 60.0) for i in range(1, 251)[::-1]]
    betas={}
    for code in df_sub.columns[:-1]:
        #get weight df
        # w1 = pd.DataFrame({code: w}, index=df_sub.index)
        # w2 = w1.copy()
        # w2.columns = ['hs300']
        # weight = w1.join(w2)
        weight=pd.DataFrame(index=df_sub.index)
        weight[code]=w
        weight['hs300']=w

        ######
        pair=df_sub[[code,'hs300']]
        pair=pair*weight
        pair=pair.dropna(axis=0,how='any') #delete those sample with NaN
        X=[]
        Y=[]
        for y,x in zip(pair[code],pair['hs300']):
            X.append([x])
            Y.append(y)
        beta=calculate_beta(X,Y)
        betas[code]=beta
    return betas


def calculate_beta(X,Y):
    regr=linear_model.LinearRegression()
    regr.fit(X,Y)
    beta=regr.coef_[0]
    return beta

def get_betas():
    df=get_df()
    month_ends=get_month_end(df)
    betas=pd.DataFrame(index=df.index,columns=df.columns[:-1])
    ###############
    t=time.time()
    ##############
    for month_end in month_ends:
        beta=get_regression_sample(df,month_end)
        beta=pd.DataFrame(beta,index=[month_end])
        betas=betas.append(beta)


        print month_end,time.time()-t
        t = time.time()
    return betas

betas=get_betas()
print betas.tail()










