#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
import numpy as np
import math


df=pd.read_csv(r'C:\data\zz800\universe_mktcap.csv',index_col=0)
df=df.set_index('stockID')
benchmark=pd.read_csv(r'C:\data\zz800\benchmark_mktcap.csv',index_col=0)
benchmark=benchmark.set_index('stockID')
benchmark_return=(benchmark['cap']*benchmark['pct_chg']).sum()/benchmark['cap'].sum()

df['benchmark_return']=benchmark_return
liq=pd.read_csv(R'C:\data\barra_factors_combined\liquidity\2016-06-30.csv',index_col=0)
df['liq']=liq['liquidity']
df['weights']=np.sqrt(df['cap'])



industry=df['sector']
new_industry=pd.DataFrame()
d=dict(industry)
for code in d:
    new_industry.at[code,d[code]]=1
new_industry=new_industry.fillna(0)

df=pd.concat([df,new_industry],axis=1)

industry_names=[f for f in df.columns[-28:]]
factors_name=['benchmark_return','liq']+industry_names
r=np.mat(df['pct_chg']).T
X=np.mat(df[factors_name])
W=np.mat(np.diag(df['weights']))
combination=(X.T*W*X).I*X.T*W
factors_return=combination*r
df2=pd.DataFrame(combination.T,index=df.index,columns=factors_name)




# r=np.mat(df['returns']).T
# X=np.mat(df[factors])
# W=np.mat(np.diag(df['weights']))
# combination2=(X.T*W*X).I*X.T*W
# factor_returns2=combination2*r
# df2=pd.DataFrame(combination2.T,index=df.index,columns=factors)
# df2=df2[['fc','bank','non_bank','other','BP','size']]
# df2.to_csv(r'c:\data\sz50\df2.csv')








