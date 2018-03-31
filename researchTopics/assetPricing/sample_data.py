# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-27  15:55
# NAME:assetPricing-sample_data.py
import pandas as pd
from dout import read_df

#figure 7.1 time series for the number of stocks
stockRetM=read_df('stockRetM','M')
stockRetM.count(axis=1).plot()

#figure 7.2 value of stocks
capM=read_df('capM','M')
capM.sum(axis=1).plot()
