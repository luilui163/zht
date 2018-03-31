import sys
sys.path.append(r'C:\zht\OneDrive\script\rf\stock_monitor')


from data import dataAPI
from data import update_pricedata
import numpy as np
import pandas as pd
import talib
import time
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import date2num
import matplotlib.collections as collections
import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.font_manager as font_manager
import matplotlib.dates as dates

def add_indicators(df):
    # notice:
    # At the first,the NaN value should be removed
    dif, dea, bar = talib.MACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    df['dif'] = dif
    df['dea'] = dea
    df['bar'] = bar * 2
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['vma20'] = df['volume'].rolling(window=20).mean()

    df['volume_mean']=df['volume'].rolling(window=20,min_periods=20).mean()
    df['volume_std']=df['volume'].rolling(window=20,min_periods=20).std()
    df['volume_zscore']=(df['volume']-df['volume_mean'])/df['volume_std']
    df['volume_signal']=0
    df.loc[(df['volume_zscore']>2),'volume_signal']=1
    df.loc[(df['volume_zscore']<-2),'volume_signal']=-1
    return df

def get_last_low_value(ind0,ind1,indicator):
    last_low=df[indicator].values[ind0]
    for i in range(ind0+1,ind1+1):
        if df[indicator].values[i]<last_low:
            last_low=df[indicator].values[i]
    return last_low

def get_last_high_value(ind0,ind1,indicator):
    last_high=df[indicator].values[ind0]
    for i in range(ind0+1,ind1+1):
        if df[indicator].values[i]>last_high:
            last_high=df[indicator].values[i]
    return last_high

def get_divergence_signal(df,smallest_total_bars):
    divergence_signal=[0]*len(df.index)

    for i in range(200,len(df.index)):
        if df['bar'].values[i]<0:
            r=0
            a1=0
            a2=0
            while True:
                r += 1
                if df['bar'].values[i-r]>=0:
                    a1=i-r+1
                    a2=i-r
                    break
            #the second while statement is used to find the bound
            while True:
                if df['bar'].values[i-r]>=0 and df['bar'].values[i-r-1]<0:
                    a3=i-r
                    a4=i-r-1
                if df['bar'].values[i-r]<0 and df['bar'].values[i-r-1]>=0:
                    a5=i-r
                    a6=i-r-1
                    break
                r+=1
            low1=get_last_low_value(a5,a4,'low')
            low2=get_last_low_value(a1,i,'low')
            bar1=get_last_low_value(a5,a4,'bar')
            bar2=get_last_low_value(a1,i,'bar')
            if low2<=low1 and bar2>bar1:
                divergence_signal[i]=1 #bottom divergence signal
        else:
            r=0
            a1=0
            a2=0
            while True:
                r += 1
                if df['bar'].values[i-r]<0:
                    a1=i-r+1
                    a2=i-r
                    break
            while True:
                if df['bar'].values[i-r]<0 and df['bar'].values[i-r-1]>=0:
                    a3=i-r
                    a4=i-r-1
                if df['bar'].values[i-r]>0 and df['bar'].values[i-r-1]<=0:
                    a5=i-r
                    a6=i-r-1
                    break
                r+=1
            high1=get_last_high_value(a5,a4,'high')
            high2=get_last_high_value(a1,i,'high')
            bar1=get_last_high_value(a5,a4,'bar')
            bar2=get_last_high_value(a1,i,'bar')
            if high2>=high1 and bar2<bar1:
                divergence_signal[i]=-1#top divergence signal
    df['divergence_signal'] = np.array(divergence_signal)
    #TODO:there should a thresh or another switch to filter the first-in divergence.
    return df

def summary_func(df,smallest_total_bars):
    df=add_indicators(df)
    df=get_divergence_signal(df,smallest_total_bars)
    return df

def get_figure(df):
    '''
     In plt's default configuration matplotlib inserts gaps in place of missing data.
     So,even we have drop the missing data in df,the figure will still plot those missing
     data.But the calculation is not affected,since they have already been processed
     before plotting.
    '''
    left, width = 0.05, 0.9
    rect1 = [left, 0.45, width, 0.5]
    rect2 = [left, 0.15, width, 0.3]
    rect3 = [left, 0.1, width, 0.05]

    fig = plt.figure(facecolor='white',figsize=(16,9))
    ax1 = fig.add_axes(rect1, axisbg='#f6f6f6')
    ax1t = ax1.twinx()
    ax2 = fig.add_axes(rect2, axisbg='#f6f6f6', sharex=ax1)
    ax3 = fig.add_axes(rect3, axisbg='#f6f6f6', sharex=ax1, ylabel='signal')

    #candlersticks
    ohlc=zip([date2num(ind) for ind in df.index],df['open'],df['high'],df['low'],df['close'])
    candlestick_ohlc(ax1,ohlc,colorup='r',colordown='g')
    # ax1.plot(df.index, df['close'], color='blue', lw=0.5,label='close price')
    ax1.plot(df.index, df['ma20'], color='darkblue', lw=0.8, label='ma20')
    leg = ax1.legend(loc='upper right', shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    ax1t.fill_between(df.index, df['volume'], 0, color='c', alpha=0.4)
    ax1t.plot(df.index,df['volume_mean'],color='orange')
    ax1t.plot(df[df['volume_zscore']>=2].index,df['volume'][df['volume_zscore']>=2],
              'v',markersize=10,color='m')
    ax1t.plot(df[df['volume_zscore']<=-2].index,df['volume'][df['volume_zscore']<=-2],
              '^',markersize=10,color='orange')
    vmax = df['volume'].max()
    ax1t.set_ylim(0, 3 * vmax)
    ax1t.set_yticks([])  # delete the yticks or can using ax1t.get_ytickslabel() then set them invisible
    ax1.set_title(stock_name)

    ax2.plot(df.index, df['dif'], color='goldenrod',alpha=0.8, label='dif')
    ax2.plot(df.index, df['dea'], color='blue', alpha=0.8,label='dea')
    ax2.plot(df.index, df['bar'], color='red', lw=1.5, label='bar')
    ax2.axhline(0, color='lime')
    ax2.text(0.025, 0.95, 'MACD ( %d, %d, %d)' % (12, 26, 9), va='top',
             transform=ax2.transAxes, fontsize=9)

    ax3.plot(df.ix[df['divergence_signal'] == 1].index, [0.2] * len(df.ix[df['divergence_signal'] == 1]),
             '^', markersize=10, color='r') #bottom divergence
    ax3.plot(df.ix[df['divergence_signal'] == -1].index, [0.8] * len(df.ix[df['divergence_signal'] ==-1]),
             'v', markersize=10, color='g') #top divergence

    ax1.fill_between(df.index, ax1.get_yticks()[0], ax1.get_yticks()[-1], where=df['bar'] < 0, color='b', alpha=0.2)
    ax2.fill_between(df.index, ax2.get_yticks()[0], ax2.get_yticks()[-1], where=df['bar'] < 0, color='b', alpha=0.2)
    ax3.fill_between(df.index, ax3.get_yticks()[0], ax3.get_yticks()[-1], where=df['bar'] < 0, color='b', alpha=0.2)

    # some yticks in defferent ax are overlapped,remove the first and last ytick of every ax.
    for ax in ax1, ax1t, ax2, ax3:
        ax.set_yticks(ax.get_yticks()[1:-1])

    for label in ax3.get_yticklabels():
        label.set_visible(False)

    for ax in ax1,ax1t,ax2,ax3:
        if ax != ax3:
            for label in ax.get_xticklabels():
                label.set_visible(False)
        else:
            for label in ax.get_xticklabels():
                label.set_rotation(30)
                label.set_horizontalalignment('right')

        ax.get_xaxis().set_major_formatter(dates.DateFormatter('%Y-%m-%d')) #set the dates format

    return fig

if __name__=='__main__':
    update_pricedata.run()
    smallest_total_bars = 3
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    stock_names=dataAPI.get_stocklist_in_database()
    monitor_result=pd.DataFrame(index=stock_names,columns=['divergence_signal','volume_signal'])
    #TODO:the suspended stockname should be removed
    for stock_name in stock_names:
        df = dataAPI.get_stock_data(stock_name, 300)
        # df.index=[ind.to_pydatetime() for ind in df.index]
        df=summary_func(df,smallest_total_bars)
        fig=get_figure(df)
        fig.savefig(r'C:\zht\OneDrive\script\rf\stock_monitor\result\%s.png'%stock_name)
        if df.index[-1].strftime('%Y%m%d')==date:#delete those suspended stocks
            monitor_result.at[stock_name,'divergence_signal']=df['divergence_signal'].values[-1]
            monitor_result.at[stock_name,'volume_signal']=df['volume_signal'].values[-1]
        monitor_result=monitor_result.replace(to_replace=0,value=np.NaN) #replace 0 with NaN,making sheet more clear
        print 'Scanning %s...'%stock_name
    monitor_result.to_csv(r'C:\zht\OneDrive\script\rf\stock_monitor\result\%s.csv' % date)



