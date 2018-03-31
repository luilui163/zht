# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 13:43:10 2016

@author: hp
"""

from EmQuantAPI import *

# 在登录函数中输入Choice账户名与密码
loginResult = c.start("cqzigl0003", "452010", "ForceLogin=1")

import pandas as pd
return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
stocks=list(return_df.columns)
stocks=[s.replace('SS','SH') for s in stocks]


data=c.css(stocks,'UNLOCKDATE,PERIODUNLOCKAMT,TOTALUNLOCKAMT,LOCKAMNT,SHARETYPE,PUNLOCKDATE,PPERIODUNLOCKAMT,PTOTALUNLOCKAMT,PLOCKAMNT').Data
print data


