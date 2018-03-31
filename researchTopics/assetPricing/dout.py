# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-11  16:24
# NAME:assetPricing-dout.py
import os
import pandas as pd
from config import DATA_PATH,BETA_PATH

def read_df(fn, freq,repository=DATA_PATH):
    '''
    read df from DATA_PATH

    :param fn:
    :return:
    '''
    df=pd.read_csv(os.path.join(repository, fn + '.csv'), index_col=0)
    df.index=pd.to_datetime(df.index).to_period(freq).to_timestamp(freq)
    #TODO:only use data after 1996
    return df.loc[df.index.year>=1996]


#TODO： are the last day of the month is the same across the csvs?