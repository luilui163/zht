# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 09:46:41 2016

@author: 13163
"""
import pandas as pd
import os

return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)

dir_name=r'c:\cq\concept\wind_new'
dates=os.listdir(dir_name)
for d in dates:
    concept_names=[os.listdir(os.path.join(dir_name,d))

sid=open(path).read().split('\n')[:-1]
stock_names=[c for c in return_df.columns]