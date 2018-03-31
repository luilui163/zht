#-*-coding: utf-8 -*-
#@author:tyhj
import numpy as np
from zht.data.gta import gtaApi
from zht.data.gta import gtaSettings
import pandas as pd
import os

mkt=gtaApi.getMkt()
mkt=mkt.sort_values(['Trdmnt','Stkcd'],ascending=[True,True]) #be sure to sort on both the date and stock code
mkt=mkt.reset_index()
g1=mkt.groupby('Stkcd')

# for g in g1:
#     name=g[0]
#     df=g[1]
#     df.to_csv(os.path.join(r'E:\aa\test\%s.csv'%name))
#     print name

mktNew=mkt.copy()
mktNew['weight']=g1[gtaSettings.mvType].shift(1)
mktNew.to_csv(r'e:\aa\mktNew.csv')












