# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:33:19 2016

@author: Administrator
"""

import os
import pandas as pd

path=r'c:\industry_change\sw\all'
files=os.listdir(path)
files_paths=[os.path.join(path,f)for f in files]
df=pd.read_csv(files_paths[0],index_col=0)
for i in range(1,len(files_paths)):
    tmp_df=pd.read_csv(files_paths[i],index_col=0)
    df=pd.concat([df,tmp_df],axis=1)
    print i
df.to_csv(r'c:\industry_change\sw\sw.csv')
