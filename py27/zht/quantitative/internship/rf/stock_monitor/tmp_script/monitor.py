#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

from data import datahandler_all

symbol='000009.SZ'
window=50
bar=datahandler_all.get_data(symbol)

bar['mean_volume']=bar['Volume'].rolling(window=window,min_periods=window).mean()
# bar['msignal']=np.sign(bar['Volume']-bar['mean_volume'])

bar['std_volume']=bar['Volume'].rolling(window=window,min_periods=window).std()
bar['zscore_volume']=(bar['Volume']-bar['mean_volume'])/bar['std_volume']

bar['signal']=0
bar.loc[(bar['zscore_volume']>2),'signal']=1
bar.loc[(bar['zscore_volume']<-2),'signal']=-1

bar.to_csv('symbol.csv')

# bar.to_csv('test.csv')

fig=plt.figure()
fig.patch.set_facecolor('white')

ax1=fig.add_subplot(211,ylabel='close price')
bar['Close'].plot(ax=ax1, color='r')


# ax2=fig.add_subplot(212,ylabel='volume')
# bar['Volume'].plot(ax=ax2,lw=1.0)
#
# ax22=ax2.twinx()
# ax22.set_ylabel('volume zscore',color='r')
# bar['zscore_volume'].plot(ax=ax22,color='r')
# #Plot the 'large volume' point
# ax22.plot(bar.ix[bar['signal']==1].index,
#          bar['zscore_volume'][bar['signal']==1],
#          '^',markersize=10,color='m')
# #Plot the 'small volume' point
# ax22.plot(bar.ix[bar['signal']==-1].index,
#          bar['zscore_volume'][bar['signal']==-1],
#          'v',markersize=10,color='k')


ax2=fig.add_subplot(212,ylabel='volume score')
bar['zscore_volume'].plot(ax=ax2,color='b')
#Plot the 'large volume' point
ax2.plot(bar.ix[bar['signal']==1].index,
         bar['zscore_volume'][bar['signal']==1],
         '^',markersize=10,color='m')
#Plot the 'small volume' point
ax2.plot(bar.ix[bar['signal']==-1].index,
         bar['zscore_volume'][bar['signal']==-1],
         'v',markersize=10,color='k')

# fig.legend(ax1,symbol)









