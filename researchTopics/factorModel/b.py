#-*-coding: utf-8 -*-
#author:tyhj
#b.py 2017.10.19 09:19


import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

df = pd.DataFrame({'a':[1,3,5,7,4,5,6,4,7,8,9],
                   'b':[3,5,6,2,4,6,7,8,7,8,9]})

reg = smf.ols('a ~ 1 + b',data=df).fit(cov_type='HAC',use_t=True,cov_kwds={'maxlags':1})
print reg.summary()


print pd.stats.ols.OLS(df.a,df.b,nw_lags=1)



