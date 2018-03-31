#-*-coding: utf-8 -*-
#@author:fudong

import pandas as pd#import packages
from data import dataApi


stockIds=dataApi.getAllstockIds()#get all the A share stock codes


historyWindow=50 #setting the history window as 50 days

volume=dataApi.getPanelDf(stockIds,'volume') #get trading volume
ret=dataApi.getReturn(stockIds,logR=False) # get stock returns
close=dataApi.getPanelDf(stockIds,'close') # get close price of all the stocks

vol=volume.dropna(axis=0,how='all') #filter the null value of volume dataframe

size=pd.read_csv(r'D:\quantDb\mkt\yearly\mkt_cap_qfq.csv',index_col=0) #get the market capitalization

size=size.dropna(axis=0,how='all') #fitler the null value in size dataframe
size.columns=[col[:6] for col in size.columns] #rename the columns of the size dataframe

newIndex=[ind.strftime('%Y-%m-%d') for ind in close.index]
size=size.reindex(newIndex)
size=size.fillna(method='ffill')
size=size.dropna(axis=0,how='all')#filter the null value in size dataframe

# columns=size.columns.tolist()
# index=size.index.tolist()
#===========================================================================================
#get table 1
avgPriceDf=pd.DataFrame(columns=['small','medium','big'])
mdPriceDf=pd.DataFrame(columns=['small','medium','big'])
avgVolumeDf=pd.DataFrame(columns=['small','medium','big'])
mdVolumeDf=pd.DataFrame(columns=['small','medium','big'])
numberDf=pd.DataFrame(columns=['small','medium','big'])# initialize the dataframe to store data

for i in range(0,len(size),historyWindow)[:-2]:
    sizeDf=size.iloc[i:i+historyWindow]
    sizeDf=sizeDf.dropna(axis=1,thresh=historyWindow*2/3) #get size dataframe for every interval

    ranks=sizeDf.iloc[-1,:].rank() #rank the stocks by size in the end of every interval

    small=ranks[len(ranks)*2/10<=ranks][ranks<len(ranks)*5/10].index #get the stock codes for small portfolio
    medium=ranks[len(ranks)*6/10<=ranks][ranks<len(ranks)*8/10].index
    big=ranks[len(ranks)*8/10<=ranks].index

    # smallPrice=close.loc[:,small].iloc[i+1:i+21] #get the stock prices for the portfolios
    # mediumPrice=close.loc[:,medium].iloc[i+1:i+21]
    # bigPrice=close.loc[:,big].iloc[i+1:i+21]


    smallPrice=close.loc[:,small].iloc[i:i+historyWindow] #get the stock prices for the portfolios
    mediumPrice=close.loc[:,medium].iloc[i:i+historyWindow]
    bigPrice=close.loc[:,big].iloc[i:i+historyWindow]

    avgPriceDf.loc[i/historyWindow,'small']=smallPrice.mean().mean() # calculate the average prices for those portfolios
    avgPriceDf.loc[i/historyWindow,'medium']=mediumPrice.mean().mean()
    avgPriceDf.loc[i/historyWindow,'big']=bigPrice.mean().mean()

    mdPriceDf.loc[i/historyWindow,'small']=smallPrice.median().median()#get median price
    mdPriceDf.loc[i/historyWindow,'medium']=mediumPrice.median().median()
    mdPriceDf.loc[i/historyWindow,'big']=bigPrice.median().median()


    smallVolume=volume.loc[:,small].iloc[i:i+historyWindow] #get volumes for portfolios
    mediumVolume=volume.loc[:,medium].iloc[i:i+historyWindow]
    bigVolume=volume.loc[:,big].iloc[i:i+historyWindow]

    # smallVolume=volume.loc[:,small].iloc[i+1:i+21] #get volumes for portfolios
    # mediumVolume=volume.loc[:,medium].iloc[i+1:i+21]
    # bigVolume=volume.loc[:,big].iloc[i+1:i+21]

    mdVolumeDf.loc[i/historyWindow,'small']=smallVolume.median().median()
    mdVolumeDf.loc[i/historyWindow,'medium']=mediumVolume.median().median()
    mdVolumeDf.loc[i/historyWindow,'big']=bigVolume.median().median()

    avgVolumeDf.loc[i / historyWindow, 'small'] = smallVolume.mean().mean()
    avgVolumeDf.loc[i / historyWindow, 'medium'] = mediumVolume.mean().mean()
    avgVolumeDf.loc[i / historyWindow, 'big'] = bigVolume.mean().mean()

    numberDf.loc[i/historyWindow,'small']=len(small)
    numberDf.loc[i/historyWindow,'medium']=len(medium)
    numberDf.loc[i/historyWindow,'big']=len(big)

    print i/historyWindow

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

# avgPriceDf.to_csv('avgPriceDf.csv')
# mdPriceDf.to_csv('mdPriceDf.csv')
# avgVolumeDf.to_csv('avgVolumeDf.csv')
# mdVolumeDf.to_csv('mdVolumeDf.csv')
# numberDf.to_csv('numberDf.csv')

panelA.to_csv('table1_panelA.csv')
panelB.to_csv('table1_panelB.csv')
panelC.to_csv('table1_panelC.csv')

#============================================================================================
#get table 2

def getPortRet(small,medium,big,type,i,historyWindow,observeWindow):
    '''
    the function is used to calculte the return of portfolio constructed by sorting volume.
    return the values in table 1
    :param small: the codes of small stocks
    :param medium: the codes of medium stocks
    :param big: the codes of big stocks
    :param type: 'small','medium','big'
    :param i: index
    :param historyWindow: defined as above
    :param observeWindow: defined as above
    :return: a tuple (rhigh,rlow,rnet)
    '''
    stock={'small':small.tolist(),
           'medium':medium.tolist(),
           'big':big.tolist()}

    df=vol.iloc[i:i+historyWindow]
    df=df.loc[:,stock[type]]
    df=df.dropna(axis=1,thresh=historyWindow*2/3)

    ranks = df.rank().iloc[-1, :]
    high = ranks[ranks < historyWindow / 10].index
    low = ranks[ranks > historyWindow * 9 / 10].index

    highReturnDf = ret.loc[:, high].iloc[i + historyWindow:i + historyWindow+observeWindow]
    lowReturnDf = ret.loc[:, low].iloc[i + historyWindow:i +historyWindow+ observeWindow]

    rhigh = (((highReturnDf + 1).cumprod().iloc[-1, :]).mean()-1)*1.0/observeWindow*100 #to percentage
    rlow = (((lowReturnDf + 1).cumprod().iloc[-1, :]).mean()-1)*1.0/observeWindow*100 #to percentage
    rlow=-rlow #short the low volume portfolio

    rnet=rhigh+rlow

    return rhigh,rlow,rnet


observeWindowSet=[1,10,20]
index=['High Volume','Low volume','Net Returns']
table2MeanDict={}
table2TDict={}
table2MeanDict['small']=pd.DataFrame(index=index,columns=observeWindowSet)
table2MeanDict['medium']=pd.DataFrame(index=index,columns=observeWindowSet)
table2MeanDict['big']=pd.DataFrame(index=index,columns=observeWindowSet)
table2TDict['small']=pd.DataFrame(index=index,columns=observeWindowSet)
table2TDict['medium']=pd.DataFrame(index=index,columns=observeWindowSet)
table2TDict['big']=pd.DataFrame(index=index,columns=observeWindowSet)

for observeWindow in observeWindowSet:
    # get the result of one column in table 1
    retDict={}
    container=pd.DataFrame(columns=['high','low','net'])
    retDict['small']=container.copy()
    retDict['medium']=container.copy()
    retDict['big']=container.copy()

    for i in range(0,len(size),historyWindow)[:-2]:
        sizeDf=size.iloc[i:i+historyWindow]
        sizeDf=sizeDf.dropna(axis=1,thresh=historyWindow*2/3)

        ranks=sizeDf.iloc[-1,:].rank()

        small=ranks[len(ranks)*2/10<=ranks][ranks<len(ranks)*5/10].index
        medium=ranks[len(ranks)*6/10<=ranks][ranks<len(ranks)*8/10].index
        big=ranks[len(ranks)*8/10<=ranks].index


        #get the return for every portfolio constructed by volume
        retDict['small'].loc[i/historyWindow]=getPortRet(small,medium,big,'small',i,historyWindow,observeWindow)
        retDict['medium'].loc[i/historyWindow]=getPortRet(small,medium,big,'medium',i,historyWindow,observeWindow)
        retDict['big'].loc[i/historyWindow]=getPortRet(small,medium,big,'big',i,historyWindow,observeWindow)

        print observeWindow,i/historyWindow

    for type in ['small','medium','big']:
        avg=retDict[type].mean()
        std=retDict[type].std()
        t=avg/std

        table2MeanDict[type].loc[:,observeWindow]=avg.values
        table2TDict[type].loc[:,observeWindow]=t.values

#save the data
map={'small':'panelA','medium':'panelB','big':'panelC'}
for key in table2MeanDict.keys():
    table2MeanDict[key].to_csv('table2_mean_%s_%s.csv'%(map[key],key))
    table2TDict[key].to_csv('table2_t_%s_%s.csv'%(map[key],key))