#-*-coding: utf-8 -*-
#@author:tyhj
from sklearn import datasets,linear_model
import pandas as pd
import numpy as np
from zht.data import data_handler
from datetime import datetime
import time
import statsmodels.api as sm

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
    df[abs(df)>0.11]=np.NaN
    return df

def get_month_end(df):
    start_date=df.index[length]
    end_date=df.index[-1]
    month_ends=pd.date_range(start_date,end_date,freq='M')
    return month_ends

def get_beta_and_hsigma(df,month_end):
    '''
    different from WLS regression,in this part ,just add weights to both the y_series,and x_series
    then,regression them.
    '''
    #get the latest 'length' days' data
    df_sub=df.truncate(after=month_end)
    df_sub=df_sub[-length:]
    df_sub=df_sub.dropna(axis=1,thresh=length*0.6)
    #get halflife weight
    w = [pow(0.5, i / 60.0) for i in range(1, 251)[::-1]]
    betas={}
    hsigmas={}
    for code in df_sub.columns[:-1]:
        #get weight df
        # w1 = pd.DataFrame({code: w}, index=df_sub.index)
        # w2 = w1.copy()
        # w2.columns = ['hs300']
        # weight = w1.join(w2)
        weight=pd.DataFrame(index=df_sub.index)
        weight[code]=w
        weight['hs300']=w
        #TODO: add the constant term to the regression equation
        ######
        regr_df=df_sub[[code,'hs300']]
        regr_df=regr_df*weight
        regr_df=regr_df.dropna(axis=0,how='any') #delete those sample with NaN

        X=np.array(regr_df['hs300'])
        X=sm.add_constant(X)
        Y=np.array(regr_df[code])
        mod = sm.OLS(Y, X).fit()
        hsigma = mod.resid.std()
        beta = mod.params[1]
        betas[code]=beta
        hsigmas[code]=hsigma
    return betas,hsigmas

def get_beta_and_hsigma1(df, month_end):
    '''
    WLS regression,
    '''
    #get the latest 'length' days' data
    df_sub=df.truncate(after=month_end)
    df_sub=df_sub[-length:]
    df_sub=df_sub.dropna(axis=1,thresh=length*0.6)
    w = [pow(0.5, i / 60.0) for i in range(1, 251)[::-1]]
    betas={}
    hsigmas={}
    for code in df_sub.columns[:-1]:
        #the last column is hs300
        regr_df=df_sub[[code,'hs300']]
        regr_df['weights']=w
        regr_df=regr_df.dropna(axis=0,how='any')#delete those sample with NaN
        X=np.array(regr_df['hs300'])
        X=sm.add_constant(X)
        Y=np.array(regr_df[code])
        #TODO:for NaN,'ffill' can also be used
        mod=sm.WLS(Y,X,weights=regr_df['weights']).fit()
        hsigma=mod.resid.std()
        beta=mod.params[1]
        betas[code]=beta
        hsigmas[code]=hsigma
    return betas,hsigmas

def get_betas():
    df=get_df()
    month_ends=get_month_end(df)
    betas=pd.DataFrame(columns=df.columns[:-1])
    hsigmas=pd.DataFrame(columns=df.columns[:-1])
    ###index=df.index can be deleted
    ###############
    t=time.time()
    ##############
    for month_end in month_ends:
        beta,hsigma=get_beta_and_hsigma1(df,month_end)
        beta=pd.DataFrame(beta,index=[month_end])
        hsigma=pd.DataFrame(hsigma,index=[month_end])
        betas=betas.append(beta)
        hsigmas=hsigmas.append(hsigma)
        print month_end,time.time()-t
        t = time.time()
    return betas,hsigmas


def run():
    BETA,hSIGMA=get_betas()
    BETA.to_csv(r'c:\data\gx\csvdata\factors\BETA1.csv')
    hSIGMA.to_csv(r'c:\data\gx\csvdata\factors\HSIGMA1.csv')

if __name__=='__main__':
    run()








