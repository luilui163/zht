#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
import numpy as np

path=r'C:\data\gx\csvdata\significance_test\tvalues.csv'

df=pd.read_csv(path,index_col=0)

df_abs=df.abs()

coefficient1=df_abs.mean()
coefficient2=df_abs[df_abs>2].count()/df_abs.count()
coefficient3
















