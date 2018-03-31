# -*- coding: utf-8 -*-
"""
Created on Fri Jul 08 14:30:54 2016

@author: 13163
"""

import pandas as pd
import numpy as np
import os

stock_ma=5


return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
return_rolling_mean_df=pd.rolling_mean(return_df,stock_ma,min_periods=int(stock_ma/2)+1)
return_rolling_std_df=pd.rolling_std(return_df,stock_ma,min_periods=int(stock_ma/2)+1)
stock_ir_df=return_rolling_mean_df/return_rolling_std_df
stock_ir_df.to_csv(r'c:\garbage\wind\stock_ir_df.csv')