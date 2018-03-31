from data import datahandler_all
import numpy as np
import talib
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.font_manager as font_manager

stock_name = '300024.SZ'
smallest_total_bars=3
df = datahandler_all.get_data(stock_name)
df = df.iloc[-1000:]


# notice:
# At the first,the NaN value should be removed

dif, dea, bar = talib.MACD(df['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
df['dif'] = dif
df['dea'] = dea
df['bar'] = bar * 2
df['ma20'] = df['Close'].rolling(window=20).mean()
df['vma20']=df['Volume'].rolling(window=20).mean()

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


last_low_close=[0.0]*len(df.index)
last_low_bar=[0.0]*len(df.index)
last_high_close=[0.0]*len(df.index)
last_high_bar=[0.0]*len(df.index)
divergence_signal=[0.0]*len(df.index)

for i in range(50,len(df.index)):
    if df['bar'].values[i]<0:
        #the first while statement is used to filter the thin cycle
        r=0
        total_positive_bars=0
        total_negetive_bars=0
        while True:
            r += 1
            if df['bar'].values[i-r]>=0:
                total_positive_bars+=1
            else:
                total_negetive_bars+=1
            if total_positive_bars>=smallest_total_bars and total_negetive_bars>=smallest_total_bars:
                break
        #the second while statement is used to find the bound
        while True:
            if df['bar'].values[i-r]<0 and df['bar'].values[i-r-1]>=0:
                break
            else:
                r+=1
        last_low_close[i]=get_last_low_value(i-r,i,'Close')
        last_low_bar[i]=get_last_low_value(i-r,i,'bar')
        if df['Close'].values[i]<=last_low_close[i] and df['bar'].values[i]>last_low_bar[i]:
            divergence_signal[i]=1 #bottom divergence signal
    else:
        r=0
        total_positive_bars=0
        total_negetive_bars=0
        while True:
            r += 1
            if df['bar'].values[i-r]>=0:
                total_positive_bars+=1
            else:
                total_negetive_bars+=1
            if total_positive_bars>=smallest_total_bars and total_negetive_bars>=smallest_total_bars:
                break
        while True:
            if df['bar'].values[i-r]>=0 and df['bar'].values[i-r-1]<0:
                break
            else:
                r+=1
        last_high_close[i]=get_last_high_value(i-r,i,'Close')
        last_high_bar[i]=get_last_high_value(i-r,i,'bar')
        if df['Close'].values[i]>=last_high_close[i] and df['bar'].values[i]<last_high_bar[i]:
            divergence_signal[i]=-1 #top divergence signal

df['divergence_signal'] = np.array(divergence_signal)

df['volume_mean']=df['Volume'].rolling(window=20,min_periods=10).mean()
df['volume_std']=df['Volume'].rolling(window=20,min_periods=20).std()
df['volume_zscore']=(df['Volume']-df['volume_mean'])/df['volume_std']
df['volume_signal']=0
df.loc[(df['volume_zscore']>2),'volume_signal']=1
df.loc[(df['volume_zscore']<-2),'volume_signal']=-1




textsize = 9
left, width = 0.05, 0.9
rect1 = [left, 0.5, width, 0.4]
rect2 = [left, 0.2, width, 0.3]
rect3 = [left, 0.1, width, 0.1]

fig = plt.figure(facecolor='white')
axescolor = '#f6f6f6'
fillcolor = 'darkgoldenrod'

ax1 = fig.add_axes(rect1, axisbg=axescolor)
ax1t = ax1.twinx()
ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
ax3 = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1, ylabel='signal')


ax1.plot(df.index, df['Close'], color='blue', label='close price')
ax1.plot(df.index, df['ma20'], color='red', lw=1.5, label='ma20')

leg = ax1.legend(loc='upper right', shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)

ax1t.fill_between(df.index, df['Volume'], 0, color='c', alpha=0.8)
# volumestd=df['Volume'].rolling(window=20).std()
# ax1t.plot(df.index,(df['Volume']-2*volumestd).rolling(20).mean(),color='darkmagenta',alpha=0.4)
# ax1t.plot(df.index,(df['Volume']+2*volumestd).rolling(20).mean(),color='darkmagenta',alpha=0.4)

ax1t.plot(df[df['volume_zscore']>=2].index,df['Volume'][df['volume_zscore']>=2],
          'v',markersize=10,color='m')
# ax1t.plot(df[df['volume_zscore']<=-2].index,df['Volume'][df['volume_zscore']<=-2],
#           '^',markersize=10,color='darkmagenta')


vmax = df['Volume'].max()
ax1t.set_ylim(0, 3 * vmax)
ax1t.set_yticks([])  # delete the yticks or can using ax1t.get_ytickslabel() then set them invisible
ax1.set_title(stock_name)

# s = '%s O:%1.2f H:%1.2f L:%1.2f C:%1.2f, V:%1.1fM Chg:%+1.2f' % (
#     today.strftime('%d-%b-%Y'),
#     last.open, last.high,
#     last.low, last.close,
#     last.volume*1e-6,
#     last.close - last.open)
# t4 = ax1.text(0.3, 0.9, s, transform=ax2.transAxes, fontsize=textsize)


ax2.plot(df.index, df['dif'], color='goldenrod',alpha=0.8, label='dif')
ax2.plot(df.index, df['dea'], color='blue', alpha=0.8,label='dea')
ax2.plot(df.index, df['bar'], color='red', lw=1.5, label='bar')
ax2.axhline(0, color='lime')
ax2.text(0.025, 0.95, 'MACD ( %d, %d, %d)' % (12, 26, 9), va='top',
         transform=ax2.transAxes, fontsize=textsize)

ax3.plot(df.ix[df['divergence_signal'] == 1].index, [0.2] * len(df.ix[df['divergence_signal'] == 1]),
         '^', markersize=20, color='r') #bottom divergence
ax3.plot(df.ix[df['divergence_signal'] == -1].index, [0.8] * len(df.ix[df['divergence_signal'] ==-1]),
         'v', markersize=20, color='g') #top divergence
# #turn off upper axis tick labels,rotate the lower ones,etc
# for ax in ax1,ax1t,ax2,ax3:
#     if ax!=ax3:
#         for label in ax.get_xticklabels():
#             label.set_visible(False)
#         else:
#             for label in ax.get_xticklabels():
#                 label.set_rotation(30)
#                 label.set_horizontalalignment('right')
#         ax.fmt_xdata=mdates.DateFormatter('%Y-%m-%d')


# ax1.fill_between(df.index,0,df['Close'].max(),where=df['macd']>=0,color='r',alpha=0.2)
ax1.fill_between(df.index, ax1.get_yticks()[0], ax1.get_yticks()[-1], where=df['bar'] < 0, color='b', alpha=0.2)
# ax2.fill_between(df.index,-0.8,0.6,where=df['macd']>=0,color='r',alpha=0.2)
ax2.fill_between(df.index, ax2.get_yticks()[0], ax2.get_yticks()[-1], where=df['bar'] < 0, color='b', alpha=0.2)
# ax3.fill_between(df.index,0,1,where=df['macd']>=0,color='r',alpha=0.2)
ax3.fill_between(df.index, ax3.get_yticks()[0], ax3.get_yticks()[-1], where=df['bar'] < 0, color='b', alpha=0.2)

# some yticks in defferent ax are overlapped,remove the first and last ytick of every ax.
for ax in ax1, ax1t, ax2, ax3:
    ax.set_yticks(ax.get_yticks()[1:-1])

for label in ax3.get_yticklabels():
    label.set_visible(False)