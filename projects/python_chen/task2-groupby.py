# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-09-25  10:02
# NAME:zht-task2-groupby.py

import pandas as pd
import numpy as np
import random


index=pd.date_range(start='2018-09-25 09:30',end='2018-09-25 11:30',freq='s')
n=sum(1 for x in index)

#create test sample
df=pd.DataFrame({
    'price':np.random.uniform(8,11,n),
    'side':[random.choice(['S','B']) for _ in range(n)],
    'volume':np.random.randint(1,1000,n)*100},
    index=index)

def stat(df):
    vol=df['volume'].sum()
    vp=np.average(df['price'],weights=df['volume'])
    buy=(df['side']=='B').sum()
    sell=(df['side']=='S').sum()
    return pd.Series([vol,vp,buy,sell],
                     index=['total_volume','vw_price',
                            'count_buy','count_sell'])

# df['min']=df.index.round('min')
# a=df.groupby(df.index.map(lambda t:t.minute)).mean()
summary=df.groupby(pd.Grouper(freq='min')).apply(stat)
last_trading=df.groupby(pd.Grouper(freq='min')).apply(lambda df:df.tail(1))
