#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
import os
import statsmodels.api as sm

def get_tvalue():
    '''
    mean :denotes the mean of abs(tValue)
    ratio:refer to the ratio of abs(t) larger than 2
    :return:
    '''
    path=r'C:\data\cj\cross_data3'
    filenames=os.listdir(path)
    tvalue_df=pd.DataFrame()
    for filename in filenames:
        date=filename[:-4]
        df=pd.read_csv(os.path.join(path,filename),index_col=0)
        df=df.dropna(axis=0,how='any')
        if len(df)>0:
            #use WLS to calculate the result
            y=df['returns']
            for factor in ['beta','momentum','nls','pb','reversion']:
                X=df[factor]
                X=sm.add_constant(X)
                #TODO:how to deal with the risk free rate
                mod=sm.WLS(y,X,weights=df['liq_market_value']).fit()
                tvalue=mod.tvalues[1]
                tvalue_df.at[date,factor]=tvalue
                print date,factor
    # tvalue_df.to_csv(r'C:\data\cj\tvalue.csv')
    mean=abs(tvalue_df).mean()
    ratio=tvalue_df[abs(tvalue_df)>2].count()/len(tvalue_df)
    return mean,ratio


def get_fval_df():
    path = r'C:\data\cj\cross_data3'
    filenames = os.listdir(path)
    tvalue_df = pd.DataFrame()
    fval_df=pd.DataFrame(columns=['beta', 'momentum', 'nls', 'pb', 'reversion'])
    for filename in filenames:
        date = filename[:-4]
        df = pd.read_csv(os.path.join(path, filename), index_col=0)
        df = df.dropna(axis=0, how='any')
        if len(df) > 0:
            #use matrix to calculate the result
            X=np.mat(df[['beta','momentum','nls','pb','reversion']])
            W=np.diag(df['liq_market_value'])
            r=np.mat(df['returns']).T
            factor_weights=(X.T*W*X).getI()*X.T*W
            fval=factor_weights*r
            s=pd.Series(np.array(fval).flatten(), index=['beta', 'momentum', 'nls', 'pb', 'reversion'])
            fval_df.loc[date]=s
        print filename
    return fval_df



def summary(fval_df):
    mean,ratio=get_tvalue()
    summary_df=pd.DataFrame()
    yearly_return_df=pd.DataFrame()
    yearly_return=fval_df.sum()/len(fval_df)*12
    yearly_std=fval_df.std()*pow(12,0.5)
    yearly_IR=yearly_return/yearly_std
    summary_df['yearly_return']=yearly_return
    summary_df['yearly_std']=yearly_std
    summary_df['yearly_IR']=yearly_IR
    summary_df['mean']=mean
    summary_df['ratio']=ratio


def plot(fval_df)
    factors=fval_df.columns
    for factor in factors:
        tmp_df=fval_df[[factor]]
        tmp_df['cumsum']=tmp_df[factor].cumsum()
        # tmp_df.index=[pd.to_datetime(ind) for ind in tmp_df.index]
        # fig, ax = plt.subplots()
        # axt = ax.twinx()
        # ax.plot(tmp_df['cumsum'])
        # axt.bar(tmp_df[factor])

        tmp_df.plot()



















