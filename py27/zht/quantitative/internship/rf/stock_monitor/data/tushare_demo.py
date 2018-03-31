#-*-coding: utf-8 -*-
#@author:tyhj

import tushare_demo as ts

df=ts.get_hist_data('000009',start='2013-01-01',end='2016-12-04')

df=ts.get_stock_basics()

df=ts.get_h_data('000009',start='2009-01-01',end='2016-12-04') # forward adjusted price

df=ts.get_today_all()
del df['name'] #delete the 'name' column to avoid encoding errors
df=df.set_index(df['code']) # set name as index,the initial index is number

df=ts.get_tick_data('000009',date='2014-01-09')

df=ts.get_today_ticks('000009')

df=ts.get_index()

df=ts.get_stock_basics()
codes=df.index.to_list()







