#-*-coding: utf-8 -*-
#@author:tyhj
import os
import pandas as pd
import numpy as np

from WindPy import *
w.start()

def get_SW_firstclass_industry():
    stock_codes=w.wset("sectorconstituent","date=2017-03-01;sectorid=a001010100000000").Data[1]
    data=w.wsd(','.join(stock_codes), "industry_sw", "2005-01-31", "2017-03-03", "industryType=1;Period=M")
    dates=[d.strftime('%Y-%m-%d') for d in data.Times]
    df=pd.DataFrame(data.Data,index=data.Codes,columns=dates)
    for date in dates:
        sub_df=df[[date]]
        sub_df.columns=['SW_firstclass_industry']
        sub_df.to_csv(os.path.join(r'C:\data\barra_factors\industry',date+'.csv'),encoding='gb2312')
        print date



