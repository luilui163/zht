#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
from data import datahandler
import matplotlib.pyplot as plt


stocklist=datahandler.get_stocklist_in_database()

for stockname in stocklist:
    dfc=datahandler.get_data(stockname)
    # dir=r'C:\zht\OneDrive\script\rf\stock_monitor\sina'
    dir=r'C:\zht\OneDrive\script\rf\stock_monitor\gx_forward'

    dfs=pd.read_csv(dir+'\\%s.csv'%stockname,index_col=0)
    dfs.index=[pd.Timestamp(nd) for nd in dfs.index]
    dfc.columns=['open','high','low','close','avgprice','turn','volume','amount','tnum']
    cols=['open','high','close','low','volume','amount']
    dfc=dfc.reindex(columns=cols)

    indc=dfc.index
    inds=dfs.index

    ind=set(indc).intersection(inds)
    ind=sorted(list(ind))
    dfs=dfs.loc[ind]
    dfc=dfc.loc[ind]

    pct=(dfs-dfc)/dfc

    ratio=pct[abs(pct)>0.001].count().sum()*1.0/(len(pct.index)*len(pct.columns))
    print stockname,1.0-ratio


    dif['close'].plot()
plt.savefig(r'C:\Users\hp\Desktop\tdx_forward.png')














