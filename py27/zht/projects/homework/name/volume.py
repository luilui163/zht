#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd


from data import dataApi

stockIds=dataApi.getAllstockIds()


# stockId=stockIds[0]

# df=dataApi.getStockDf(stockId)
# print df.head()

historyWindow=50
observeWindow=20


volume=dataApi.getPanelDf(stockIds,'volume')
ret=dataApi.getReturn(stockIds,logR=False)
close=dataApi.getPanelDf(stockIds,'close')

vol=volume.dropna(axis=0,how='all')

def getPortRet(small,medium,big,type,i):
    global historyWindow,observeWindow

    stock={'small':small.tolist(),
           'medium':medium.tolist(),
           'big':big.tolist()}

    df=vol.iloc[i:i+historyWindow]
    df=df.loc[:,stock[type]]
    df=df.dropna(axis=1,thresh=historyWindow*2/3)

    ranks = df.rank().iloc[-1, :]
    high = ranks[ranks < historyWindow / 10].index
    low = ranks[ranks > historyWindow * 9 / 10].index

    highReturnDf = ret.loc[:, high].iloc[i + 1:i + 21]
    lowReturnDf = ret.loc[:, low].iloc[i + 1:i + 21]

    rhigh = ((highReturnDf + 1).cumprod().iloc[-1, :]).mean()-1
    rlow = ((lowReturnDf + 1).cumprod().iloc[-1, :]).mean()-1
    rnet=rhigh-rlow

    return rhigh,rlow,rnet



size=pd.read_csv(r'D:\quantDb\mkt\yearly\mkt_cap_qfq.csv',index_col=0)

size=size.dropna(axis=0,how='all')
size.columns=[col[:6] for col in size.columns]

newIndex=[ind.strftime('%Y-%m-%d') for ind in close.index]
size=size.reindex(newIndex)
size=size.fillna(method='ffill')
size=size.dropna(axis=0,how='all')

columns=size.columns.tolist()
index=size.index.tolist()


#get table 1
avgPriceDf=pd.DataFrame(columns=['small','medium','big'])
mdPriceDf=pd.DataFrame(columns=['small','medium','big'])
avgVolumeDf=pd.DataFrame(columns=['small','medium','big'])
mdVolumeDf=pd.DataFrame(columns=['small','medium','big'])

numberDf=pd.DataFrame(columns=['small','medium','big'])

retDict={}
container=pd.DataFrame(columns=['high','low','net'])
retDict['small']=container
retDict['medium']=container
retDict['big']=container


for i in range(0,len(size),historyWindow)[:-2]:
    sizeDf=size.iloc[i:i+historyWindow]
    sizeDf=sizeDf.dropna(axis=1,thresh=historyWindow*2/3)

    ranks=sizeDf.iloc[-1,:].rank()

    small=ranks[len(ranks)*2/10<=ranks][ranks<len(ranks)*5/10].index
    medium=ranks[len(ranks)*6/10<=ranks][ranks<len(ranks)*8/10].index
    big=ranks[len(ranks)*8/10<=ranks].index

    retDict['small'].loc[i/50]=getPortRet(small,medium,big,'small',i)
    retDict['medium'].loc[i/50]=getPortRet(small,medium,big,'medium',i)
    retDict['big'].loc[i/50]=getPortRet(small,medium,big,'big',i)


    smallPrice=close.loc[:,small].iloc[i+1:i+21]
    mediumPrice=close.loc[:,medium].iloc[i+1:i+21]
    bigPrice=close.loc[:,big].iloc[i+1:i+21]

    avgPriceDf.loc[i/50,'small']=smallPrice.mean().mean()
    avgPriceDf.loc[i/50,'medium']=mediumPrice.mean().mean()
    avgPriceDf.loc[i/50,'big']=bigPrice.mean().mean()

    mdPriceDf.loc[i/50,'small']=smallPrice.median().median()
    mdPriceDf.loc[i/50,'medium']=mediumPrice.median().median()
    mdPriceDf.loc[i/50,'big']=bigPrice.median().median()

    smallVolume=volume.loc[:,small].iloc[i+1:i+21]
    mediumVolume=volume.loc[:,medium].iloc[i+1:i+21]
    bigVolume=volume.loc[:,big].iloc[i+1:i+21]

    mdVolumeDf.loc[i/50,'small']=smallVolume.median().median()
    mdVolumeDf.loc[i/50,'medium']=mediumVolume.median().median()
    mdVolumeDf.loc[i/50,'big']=bigVolume.median().median()

    avgVolumeDf.loc[i / 50, 'small'] = smallVolume.mean().mean()
    avgVolumeDf.loc[i / 50, 'medium'] = mediumVolume.mean().mean()
    avgVolumeDf.loc[i / 50, 'big'] = bigVolume.mean().mean()

    numberDf.loc[i/50,'small']=len(small)
    numberDf.loc[i/50,'medium']=len(medium)
    numberDf.loc[i/50,'big']=len(big)

    print i/50

#table1
#panel A
panelA=pd.DataFrame(columns=['Small Firms','Medium Firms','Large Firms'])
panelA.loc['Average stock price']=avgPriceDf.mean().values
panelA.loc['Median stock price']=mdPriceDf.median().values
panelA.loc['Average volume']=avgVolumeDf.mean().values
panelA.loc['Median volume']=mdVolumeDf.median().values

#panel B
panelB=pd.DataFrame(columns=['Small Firms','Medium Firms','Large Firms'])
panelB.loc['stocks in subsample']=numberDf.iloc[0].values
panelB.loc['Average stock price']=avgPriceDf.iloc[0].values
panelB.loc['Median stock price']=mdPriceDf.iloc[0].values
panelB.loc['Average volume']=avgVolumeDf.iloc[0].values
panelB.loc['Median volume']=mdVolumeDf.iloc[0].values

#panel C
panelC=pd.DataFrame(columns=['Small Firms','Medium Firms','Large Firms'])
panelC.loc['stocks in subsample']=numberDf.iloc[-1].values
panelC.loc['Average stock price']=avgPriceDf.iloc[-1].values
panelC.loc['Median stock price']=mdPriceDf.iloc[-1].values
panelC.loc['Average volume']=avgVolumeDf.iloc[-1].values
panelC.loc['Median volume']=mdVolumeDf.iloc[-1].values


avgPriceDf.to_csv('avgPriceDf.csv')
mdPriceDf.to_csv('mdPriceDf.csv')
avgVolumeDf.to_csv('avgVolumeDf.csv')
mdVolumeDf.to_csv('mdVolumeDf.csv')
numberDf.to_csv('numberDf.csv')


panelA.to_csv('panelA.csv')
panelB.to_csv('panelB.csv')
panelC.to_csv('panelC.csv')


retDict['small'].to_csv('small.csv')
retDict['medium'].to_csv("medium.csv")
retDict['big'].to_csv('big.csv')




#get table 2





