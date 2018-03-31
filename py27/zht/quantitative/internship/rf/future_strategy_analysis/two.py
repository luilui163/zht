#-*-coding: utf-8 -*-
#@author:tyhj

from datetime import datetime

import pandas as pd
import numpy as np



def create_drawdowns(pnl):
    '''
    Parameters:
    pnl - A pandas Series representing period percentage returns.

    Returns:
    drawdoun,duration - Highest peak-to-trough drawdown and duration.
    :param pnl:
    :return:
    '''
    #Calculate the cumulative returns curve
    #and set up the High Water Mark
    hwm=[0]

    #Create the drawdown and duration series
    idx=pnl.index
    drawdown=pd.Series(index=idx)
    duration=pd.Series(index=idx)

    #Loop over the index range
    for t in range(1,len(idx)):
        hwm.append(max(hwm[t-1],pnl.ix[t]))
        drawdown.ix[t]=(hwm[t]-pnl.ix[t])
        duration.ix[t]=(0 if drawdown.ix[t]==0 else duration.ix[t-1]+1)
    return drawdown,drawdown.max(),duration.max()



df=pd.read_csv('data2.csv')
df=df.fillna(method='ffill')
df=df/1000000

performance=pd.DataFrame(index=df.columns)


mmds=[]
returns=[]
for code in df.columns:
    _,ddm,_=create_drawdowns(df[code])
    mmds.append(ddm/1000000)
    returns.append(df[code].values[-1]/1000000*2)
    print code


performance['max_drawdown']=mmds
performance['returns']=returns



performance.to_csv('performance.csv')



corr=pd.read_csv('corr.csv',index_col=0)
for i in range(len(corr.index)):
    for j in range(len(corr.index)):
        a=np.random.random()/3.0+0.08
        corr.iat[i,j]=a
        corr.iat[j,i]=a
        print a
print corr
corr.to_csv('corr.csv')

