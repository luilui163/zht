#-*-coding: utf-8 -*-
#author:tyhj
#calBeta.py 2017.10.18 15:11

import pandas as pd
import numpy as np
import os


from zht.data.gta import gtaApi
from zht.util import pandasu
from zht.util import statu
from zht.util.pandasu import winsorize

from zht.researchTopics.factorModel.beta.params import *


def usingDailyData():
    '''
    use the daily returns to calculate beta,month by month

    Returns:

    '''
    dict1={'1M':15,'3M':50,'6M':100,'12M':200,'24M':450}

    rets=gtaApi.get_stockRetD()
    retm=gtaApi.get_mktRetD()
    rf=gtaApi.get_rf(freq='D')

    rets,retm,rf=pandasu.get_inter_index([rets,retm,rf])

    erets=rets.sub(rf['rf'],axis=0)
    eretm=retm.sub(rf['rf'],axis=0)

    sids=erets.columns.tolist()
    months=erets.resample('M').last().index.tolist()

    cmb=erets.copy(deep=True)
    cmb['eretm']=eretm.iloc[:,0]

    for length,thresh in dict1.iteritems():
        betadf=pd.DataFrame()
        r2df=pd.DataFrame()
        # sids=sids[:30]#TODO
        for month in months:
            tmpdf=cmb.loc[:month,:]
            for sid in sids:
                regdf=tmpdf.loc[:,[sid,'eretm']]
                regdf=regdf.last(length)
                regdf=regdf.dropna(how='any',axis=0)
                if regdf.shape[0]>thresh:
                    coefs,tvalues,r2,resids=pandasu.reg(regdf)
                    betadf.loc[month.strftime('%Y-%m-%d'),sid]=coefs[1]
                    # do not use loc when the index is timestamp
                    r2df.loc[month.strftime('%Y-%m-%d'),sid]=r2
            print month
        betadf.to_csv(os.path.join(betap,length+'.csv'))
        r2df.to_csv(os.path.join(betap,length+'_r2.csv'))

def usingMonthlyData():
    '''
    calculate betas by using monthly return,month by month.
    Returns:

    '''
    dict2={'12M':10,'24M':20,'36M':24,'60M':24}
    rets=gtaApi.get_stockRetM(recal=True)
    retm=gtaApi.get_mktRetM(recal=True)
    rf=gtaApi.get_rf(freq='M')

    rets,retm,rf=pandasu.get_inter_index([rets,retm,rf])

    erets = rets.sub(rf['rf'], axis=0)
    eretm = retm.sub(rf['rf'], axis=0)

    sids=erets.columns.tolist()
    months=erets.index.tolist()

    cmb = erets.copy(deep=True)
    cmb['eretm'] = eretm.iloc[:, 0]

    for length, thresh in dict2.iteritems():
        betadf = pd.DataFrame()
        r2df = pd.DataFrame()
        # sids=sids[:30]#TODO
        for month in months:
            tmpdf = cmb.loc[:month, :]
            for sid in sids:
                regdf = tmpdf.loc[:, [sid, 'eretm']]
                regdf = regdf.last(length)
                regdf = regdf.dropna(how='any', axis=0)
                if regdf.shape[0] > thresh:
                    coefs, tvalues, r2, resids = pandasu.reg(regdf)
                    betadf.loc[month.strftime('%Y-%m-%d'), sid] = coefs[1]
                    # do not use loc when the index is timestamp
                    r2df.loc[month.strftime('%Y-%m-%d'), sid] = r2
            print month

        name=str(int(length[:-1])/12)+'Y'
        betadf.to_csv(os.path.join(betap, name + '.csv'))
        r2df.to_csv(os.path.join(betap, name + '_r2.csv'))

def summary():
    names=['1M','3M','6M','12M','24M','1Y','2Y','3Y','5Y']
    summarydf=pd.DataFrame()
    for name in names:
        df=pd.read_csv(os.path.join(betap,name+'.csv'),
                       index_col=0,parse_dates=True)
        s=statu.summary_statistics(df)
        s.to_csv(os.path.join(betap,'summary_%s.csv'%name))
        # #winsorize the values before calculate the averages,since there are some extreme values
        # s=pandasu.winsorize(s,(0.05,0.05),axis=0)
        summarydf[name]=s.mean()
        print name
    summarydf.to_csv(os.path.join(betap,'summary.csv'))

def correlation():
    '''
    This table presents the time-series averages of the cross-sectional
    Pearson product-moment (below-diagonal entries) and Spearman rank
    (above-diagonal entries) correlations between pairs of variables
    measuring market beta.

    Returns:

    '''
    names=['1M','3M','6M','12M','24M','1Y','2Y','3Y','5Y']
    dfs=[pd.read_csv(os.path.join(betap,name+'.csv'),
         index_col=0,parse_dates=True) for name in names]
    # dfs=[pd.read_csv(os.path.join(r'D:\quantDb\researchTopics\factorModel\beta\%s.csv'%name),
    #                  index_col=0,parse_dates=True) for name in names]
    dfs=pandasu.get_inter_frame(dfs)
    months=dfs[0].index.tolist()

    corrpAvg=pd.DataFrame()
    corrsAvg=pd.DataFrame()
    for month in months:
        corrdf=pd.DataFrame()
        for i in range(len(dfs)):
            corrdf[names[i]]=dfs[i].loc[month]

        corrs = statu.corr(corrdf, 'spearman',winsorize=False)
        corrp=statu.corr(corrdf,'pearson',winsorize = True)

        corrpAvg+=corrp
        corrsAvg+=corrs
        print month
    corrpAvg = corrpAvg / (len(months) * 1.0)
    corrsAvg = corrsAvg / (len(months) * 1.0)

    corr1=np.tril(corrpAvg.values,k=-1)
    corr2=np.triu(corrsAvg.values,k=1)

    corr=pd.DataFrame(corr1+corr2,index=corrpAvg.index,columns=corrpAvg.columns)
    np.fill_diagonal(corr.values,np.NaN)
    corr.to_csv(os.path.join(betap,'corr.csv'))
    corrpAvg.to_csv(os.path.join(betap,'corr_pearson.csv'))
    corrsAvg.to_csv(os.path.join(betap,'corr_spearman.csv'))

    # corr.to_csv(r'D:\quantDb\researchTopics\factorModel\beta\corr.csv')
    # corrpAvg.to_csv(r'D:\quantDb\researchTopics\factorModel\beta\corr_pearson.csv')
    # corrsAvg.to_csv(r'D:\quantDb\researchTopics\factorModel\beta\corr_spearman.csv')

def calculate_persistence():
    names = ['1M', '3M', '6M', '12M', '24M', '1Y', '2Y', '3Y', '5Y']
    dfs = [pd.read_csv(os.path.join(betap,name+'.csv'),
                       index_col=0, parse_dates=True) for name in names]
    # dfs = [pd.read_csv(os.path.join(r'D:\quantDb\researchTopics\factorModel\beta\%s.csv' % name),
    #                    index_col=0, parse_dates=True) for name in names]
    perdf=pd.DataFrame()
    for i in range(len(names)):
        per=statu.persistence(dfs[i],offsets=[1,3,6,12,24,36,48,60,120])
        perdf[names[i]]=per
        print names[i]
    # perdf.to_csv(r'D:\quantDb\researchTopics\factorModel\beta\persistence.csv')
    perdf.to_csv(os.path.join(betap,'persistence.csv'))

def breakPoints_and_countGroups():
    q=10
    names = ['1M', '3M', '6M', '12M', '24M', '1Y', '2Y', '3Y', '5Y']
    for name in names:
        df=pd.read_csv(os.path.join(betap,name+'.csv'),index_col=0,parse_dates=True)

        # df=pd.read_csv(r'D:\quantDb\researchTopics\factorModel\beta\%s.csv' % name,
        #             index_col=0,parse_dates=True)
        bps=statu.cal_breakPoints(df,q)
        bps.to_csv(os.path.join(betap,'breakPoints_%s.csv'%name))
        # bps.to_csv(r'D:\quantDb\researchTopics\factorModel\beta\breakPoints_%s.csv'%name)
        count=statu.count_groups(df,q)
        count.to_csv(os.path.join(betap,'count_%s.csv'%name))
        # count.to_csv(r'D:\quantDb\researchTopics\factorModel\beta\count_%s.csv'%name)
        print name
    #TODO:In fact,the count is not exactly the number of stocks to calculate the weighted return
    #TODO:as some stocks will be deleted due to the missing of weights.

def portfolioEret(q=10):
    '''
    calculate the portfolio excess returns
    Args:
        q:

    Returns:

    '''

    rets = gtaApi.get_stockRetM(recal=True)
    rf = gtaApi.get_rf(freq='M')
    mktCap = gtaApi.get_sizeM(recal=True)

    rets.columns = [str(col) for col in rets.columns]
    mktCap.columns = [str(col) for col in mktCap.columns]

    erets = rets.sub(rf['rf'], axis=0)

    def _wavg(df):
        if df.shape[0]>0:
            d=df['ret']
            w=df['weight']
            return np.average(d,weights=w)
        else:
            return None
    def _eavg(df):
        if df.shape[0]>0:
            return np.average(df['ret'])

    names = ['1M', '3M', '6M', '12M', '24M', '1Y', '2Y', '3Y', '5Y']
    for name in names:
        df=pd.read_csv(r'D:\quantDb\researchTopics\factorModel\beta\%s.csv'%name,
                       index_col=0,parse_dates=True)
        #TODO: do not need rf here
        df,erets,rf,mktCap=pandasu.get_inter_index([df,erets,rf,mktCap])
        months=df.index.tolist()
        eret_wavg=pd.DataFrame(columns=['g' + str(i) for i in range(1, q + 1)])
        eret_eavg=pd.DataFrame(columns=['g' + str(i) for i in range(1, q + 1)])
        for t in range(len(months)-1):
            g=pd.qcut(df.loc[months[t]],q,
                      labels=['g' + str(i) for i in range(1, q + 1)])
            r=erets.loc[months[t+1]]
            w=mktCap.loc[months[t]]#the weight is the market capitalization of time t

            r.name='ret'
            w.name='weight'
            g.name='group'

            comb1=pd.concat([r,w,g],axis=1)
            comb1=comb1.dropna(axis=0,how='any')
            wavgs=comb1.groupby('group').apply(_wavg)
            eret_wavg.loc[months[t]]=wavgs

            comb2=pd.concat([r,g],axis=1)
            comb2=comb2.dropna(axis=0,how='any')
            eavgs=comb2.groupby('group').apply(_eavg)
            eret_eavg.loc[months[t]]=eavgs
            print name,months[t]

        eret_wavg['g%s-g1'%q]=eret_wavg['g%s'%q]-eret_wavg['g1']
        eret_wavg.index.name='t'
        eret_wavg['t+1']=months[1:]
        cols=['t+1']+[col for col in eret_wavg.columns if col!='t+1']
        eret_wavg=eret_wavg.reindex_axis(cols,axis=1)
        eret_wavg.to_csv(os.path.join(betap,'eret_wavg_%s.csv'%name))
        # eret_wavg.to_csv(r'D:\quantDb\researchTopics\factorModel\beta\eret_wavg_%s.csv'%name)

        eret_eavg['g%s-g1'%q]=eret_eavg['g%s'%q]-eret_eavg['g1']
        eret_eavg.index.name='t'
        eret_eavg['t+1']=months[1:]
        cols=['t+1']+[col for col in eret_eavg.columns if col!='t+1']
        eret_eavg=eret_eavg.reindex_axis(cols,axis=1)
        eret_eavg.to_csv(os.path.join(betap,'eret_eavg_%s.csv'%name))
        # eret_eavg.to_csv(r'D:\quantDb\researchTopics\factorModel\beta\eret_eavg_%s.csv'%name)


if __name__=="__main__":
    usingMonthlyData()
    usingMonthlyData()
    summary()
    correlation()
    calculate_persistence()
    breakPoints_and_countGroups()
    portfolioEret()



# import statsmodels.formula.api as smf
#
# df = pd.DataFrame({'a':[1,3,5,7,4,5,6,4,7,8,9],
#                    'b':[3,5,6,2,4,6,7,8,7,8,9]})
#
# reg = smf.ols('a ~ 1 + b',data=df).fit(cov_type='HAC',cov_kwds={'maxlags':1})
# print reg.summary()







# from zht.researchTopics.factorModel.classicalModels import *
#
# capm=get_capm()
#
# print capm.head()






