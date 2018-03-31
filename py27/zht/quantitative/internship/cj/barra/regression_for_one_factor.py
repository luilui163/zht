#-*-coding: utf-8 -*-
#@author:tyhj

from zht.data import data_handler
import os
import pandas as pd
import numpy as np
from sklearn import datasets,linear_model
import statsmodels.api as sm


def get_tvalues_df():
    factor_path=r'C:\data\gx\csvdata\normalized_factors'
    filenames=os.listdir(factor_path)
    returns=pd.read_csv(r'C:\data\gx\csvdata\month_returns.csv',index_col=0)

    tvalues_df=pd.DataFrame()
    for fn in filenames:
        factor_name=fn[:-4]
        factor_df=pd.read_csv(os.path.join(factor_path,fn),index_col=0)

        # since we need to use time to predict time t+1,for more details,refer to the paper
        factor_df=factor_df.shift(1)

        # if the sample is too small the result may be biased,so delete these sample
        factor_df=factor_df.dropna(axis=0,thresh=50)
        ind1=factor_df.index
        ind2=returns.index
        ind=[d for d in ind2 if d in ind1]

        tvalue_series=pd.Series()
        for regression_date in ind:
            regr_df=pd.DataFrame()
            factor_series=factor_df.loc[regression_date]
            returns_series=returns.loc[regression_date]
            regr_df[factor_name]=factor_series.shift(1)
            regr_df['returns']=returns_series
            regr_df=regr_df.dropna(axis=0,how='any')#delete the NaN value

            # TODO:should the regr_df['returns'] be shifted forward by one period?
            # TODO:set the weight as the market size
            X=np.array(regr_df[factor_name])
            X=sm.add_constant(X)
            Y=np.array(regr_df['returns'])
            res=sm.WLS(Y,X,weights=1).fit()
            tvalue=res.tvalues[1]
            tvalue_series.loc[regression_date]=tvalue
            print factor_name,regression_date
        tvalues_df[factor_name]=tvalue_series
    return tvalues_df



tvalues_df=get_tvalues_df()

tvalues_df.to_csv(r'C:\data\gx\csvdata\significance_test\tvalues.csv')












