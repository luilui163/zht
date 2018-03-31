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
df = datahandler_all.get_data(stock_name)
df = df.iloc[-500:]


# notice:
# At the first,the NaN value should be removed

dif, dea, hist = talib.MACD(df['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
df['dif'] = dif
df['dea'] = dea
df['macd'] = hist * 2
df['ma20'] = df['Close'].rolling(window=20).mean()
df['vma20']=df['Volume'].rolling(window=20).mean()



idx = df.index
macd_wm = [0.0] * len(idx)
for i in range(1, len(idx)):
    if df['macd'].values[i] >= 0:
        if df['macd'].values[i] >= macd_wm[i - 1]:
            macd_wm[i] = df['macd'].values[i]
        else:
            macd_wm[i] = macd_wm[i - 1]
    else:
        if df['macd'].values[i] < macd_wm[i - 1]:
            macd_wm[i] = df['macd'].values[i]
        else:
            macd_wm[i] = macd_wm[i - 1]

df['macd_wm'] = np.array(macd_wm)

close_wm = [0.0] * len(idx)
for i in range(1, len(idx)):
    if df['macd'].values[i] >= 0:
        if df['Close'].values[i] > close_wm[i - 1]:
            close_wm[i] = df['Close'].values[i]
        else:
            close_wm[i] = close_wm[i - 1]
    if df['macd'].values[i] < 0:
        if df['Close'].values[i] < close_wm[i - 1]:
            close_wm[i] = df['Close'].values[i]
        else:
            close_wm[i] = close_wm[i - 1]

df['close_wm'] = np.array(close_wm)

smallest_cycle_window = 20
divergence_signal = [0]
for i in range(1, len(idx)):
    if df['macd_wm'].values[i] <= 0:
        last_low_close = 0
        last_low_macd = 0
        r = smallest_cycle_window
        while True:
            if df['macd'].values[i - r] >= 0:
                r += 1
            else:
                last_low_close = df['close_wm'].values[i - r]
                last_low_macd = df['macd_wm'].values[i - r]
                break
        if df['Close'].values[i] < last_low_close and df['macd'].values[i] >= last_low_macd:
            divergence_signal.append(1)
        else:
            divergence_signal.append(0)
    else:
        last_high_close = 0
        last_high_macd = 0
        r = smallest_cycle_window
        while True:
            if df['macd'].values[i - r] < 0:
                r += 1
            else:
                last_high_close = df['close_wm'].values[i-r]
                last_high_macd=df['macd_wm'].values[i-r]
                break
        if df['Close'].values[i]>last_high_close and df['macd'].values[i]<=last_high_close:
            divergence_signal.append(-1)
        else:
            divergence_signal.append(0)
    print i

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
ax2.plot(df.index, df['macd'], color='red', lw=1.5, label='bar')
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
ax1.fill_between(df.index, ax1.get_yticks()[0], ax1.get_yticks()[-1], where=df['macd'] < 0, color='b', alpha=0.2)
# ax2.fill_between(df.index,-0.8,0.6,where=df['macd']>=0,color='r',alpha=0.2)
ax2.fill_between(df.index, ax2.get_yticks()[0], ax2.get_yticks()[-1], where=df['macd'] < 0, color='b', alpha=0.2)
# ax3.fill_between(df.index,0,1,where=df['macd']>=0,color='r',alpha=0.2)
ax3.fill_between(df.index, ax3.get_yticks()[0], ax3.get_yticks()[-1], where=df['macd'] < 0, color='b', alpha=0.2)

# some yticks in defferent ax are overlapped,remove the first and last ytick of every ax.
for ax in ax1, ax1t, ax2, ax3:
    ax.set_yticks(ax.get_yticks()[1:-1])

for label in ax3.get_yticklabels():
    label.set_visible(False)