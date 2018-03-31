#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
from data import datahandler
import matplotlib.pyplot as plt


stocklist=datahandler.get_stocklist_in_database()

for stockname in stocklist:
    df1=datahandler.get_data(stockname)
    # dir=r'C:\zht\OneDrive\script\rf\stock_monitor\sina'
    dir=r'C:\zht\OneDrive\script\rf\stock_monitor\gx_forward'

    df2=pd.read_csv(dir+'\\%s.csv'%stockname,index_col=0)
    df2.index=[pd.Timestamp(nd) for nd in df2.index]
    df1.columns=['open','high','low','close','avgprice','turn','volume','amount','tnum']
    cols=['open','high','close','low','volume','amount']
    df1=df1.reindex(columns=cols)

    indc=df1.index
    inds=df2.index

    ind=set(indc).intersection(inds)
    ind=sorted(list(ind))
    df2=df2.loc[ind]
    df1=df1.loc[ind]

    pct=(df2-df1)/df1

    ratio=pct[abs(pct)>0.001].count().sum()*1.0/(len(pct.index)*len(pct.columns))
    print stockname,1.0-ratio


    dif['close'].plot()
plt.savefig(r'C:\Users\hp\Desktop\tdx_forward.png')














