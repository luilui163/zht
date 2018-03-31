#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np

#去极值
def winsorize(df,factor):
    sub_df = df[[factor]]
    sub_df[sub_df > np.percentile(sub_df, 95)] = np.percentile(sub_df, 95)
    sub_df[sub_df < np.percentile(sub_df, 5)] = np.percentile(sub_df, 5)
    return sub_df









