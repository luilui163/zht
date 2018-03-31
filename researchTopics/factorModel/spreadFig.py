#-*-coding: utf-8 -*-
#author:tyhj
#spreadFig.py 2017/10/2 10:31

import pandas as pd

from zht.util.plotu import plotCumulativeRet

from params import *

fns=os.listdir(idrp)


returns=pd.DataFrame(columns=['averageRet'])
for i,fn in enumerate(fns):
    df=pd.read_csv(os.path.join(idrp,fn),index_col=0)
    spread=df.iloc[:,-1]-df.iloc[:,0]
    returns.loc[fn[:-4],'averageRet']=spread.mean()
    fig=plotCumulativeRet(spread)
    fig.savefig(os.path.join(spfp,fn[:-4]+'.png'))
    print i
returns['averageRet_abs']=returns['averageRet'].abs()
returns=returns.sort_values('averageRet_abs',ascending=False)
returns.to_csv(os.path.join(cpfp,'spreadAverageRet.csv'))





