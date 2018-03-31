# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-12  09:14
# NAME:assetPricing-size.py
import os
import pandas as pd
from config import SIZE_PATH,DATA_PATH
import numpy as np
from zht.utils import assetPricing
from zht.utils.assetPricing import summary_statistics, cal_breakPoints, count_groups
from zht.utils.mathu import get_inter_frame

from dout import read_df

def cal_sizes():
    '''
    compute variety of sizes

    :return:
    '''
    mktCap=read_df('capM',freq='M')

    mktCap.to_csv(os.path.join(SIZE_PATH, 'mktCap.csv'))

    size=np.log(mktCap)
    size.to_csv(os.path.join(SIZE_PATH,'size.csv'))

    # junes=[m for m in mktCap.index.tolist() if m.split('-')[1]=='06']
    mths=[m for m in mktCap.index.tolist() if m.month==6]+[mktCap.index[-1]]
    junesDf=mktCap.loc[mths]
    mktCap_ff=junesDf.resample('M').ffill()
    mktCap_ff.to_csv(os.path.join(SIZE_PATH,'mktCap_ff.csv'))

    size_ff=np.log(mktCap_ff)
    size_ff.to_csv(os.path.join(SIZE_PATH,'size_ff.csv'))

def summary():
    names=['mktCap','size','mktCap_ff','size_ff']
    series=[]
    for name in names:
        df=pd.read_csv(os.path.join(SIZE_PATH,name+'.csv'),index_col=0)
        s=summary_statistics(df,axis=1)
        s.to_csv(os.path.join(SIZE_PATH,'summary_%s.csv'%name))
        series.append(s.mean())
    pd.concat(series,keys=names,axis=1).to_csv(os.path.join(SIZE_PATH,'summary.csv'))

def correlation():
    '''
    This table presents the time-series averages of the cross-sectional
    Pearson product-moment (below-diagonal entries) and Spearman rank
    (above-diagonal entries) correlations between pairs of variables
    measuring market beta.

    Returns:

    '''
    names=['mktCap','size','mktCap_ff','size_ff']
    dfs=[pd.read_csv(os.path.join(SIZE_PATH,name+'.csv'),
         index_col=0,parse_dates=True) for name in names]
    # dfs=[pd.read_csv(os.path.join(r'D:\quantDb\researchTopics\factorModel\beta\%s.csv'%name),
    #                  index_col=0,parse_dates=True) for name in names]
    dfs=get_inter_frame(dfs)
    months=dfs[0].index.tolist()

    # corrpAvg=pd.DataFrame()
    # corrsAvg=pd.DataFrame()
    corrss=[]
    corrps=[]
    for month in months:
        corrdf=pd.DataFrame()
        for i in range(len(dfs)):
            corrdf[names[i]]=dfs[i].loc[month]

        corrs = assetPricing.corr(corrdf, 'spearman',winsorize=False)
        corrp=assetPricing.corr(corrdf,'pearson',winsorize = True)

        corrss.append(corrs)
        corrps.append(corrp)

        # corrpAvg+=corrp
        # corrsAvg+=corrs
        print(month)
    # corrpAvg = corrpAvg / (len(months) * 1.0)
    # corrsAvg = corrsAvg / (len(months) * 1.0)
    s_concat=pd.concat(corrss)
    corrsAvg=s_concat.groupby(s_concat.index).mean()
    corrsAvg=corrsAvg.reindex(corrsAvg.columns)

    p_concat=pd.concat(corrps)
    corrpAvg=p_concat.groupby(p_concat.index).mean()
    corrpAvg=corrpAvg.reindex(corrpAvg.columns)

    corr1=np.tril(corrpAvg.values,k=-1)
    corr2=np.triu(corrsAvg.values,k=1)

    corr=pd.DataFrame(corr1+corr2,index=corrpAvg.index,columns=corrpAvg.columns)
    np.fill_diagonal(corr.values,np.NaN)
    corr.to_csv(os.path.join(SIZE_PATH,'corr.csv'))
    corrpAvg.to_csv(os.path.join(SIZE_PATH,'corr_pearson.csv'))
    corrsAvg.to_csv(os.path.join(SIZE_PATH,'corr_spearman.csv'))

def calculate_persistence():
    names=['mktCap','size','mktCap_ff','size_ff']
    dfs = [pd.read_csv(os.path.join(SIZE_PATH,name+'.csv'),
                       index_col=0,) for name in names]
    perdf=pd.DataFrame()
    for i in range(len(names)):
        per=assetPricing.persistence(dfs[i],offsets=[1,3,6,12,24,36,48,60,120])
        perdf[names[i]]=per
    perdf.to_csv(os.path.join(SIZE_PATH,'persistence.csv'))

def get_percent_ratio():
    df=pd.read_csv(os.path.join(SIZE_PATH,'mktCap.csv'),index_col=0)
    def get_ratio(s):
        ratios=[1,5,10,25]
        return pd.Series([s.nlargest(r).sum()/s.sum() for r in ratios],
                         index=ratios)
    r=df.apply(get_ratio,axis=1)
    r.index=r.index.to_datetime().to_period('M')
    fig=r[40:].plot().get_figure()
    fig.savefig(os.path.join(SIZE_PATH,'percent of market value.png'))

#TODO: trim the samples from 1996?

def breakPoints_and_countGroups():
    q=10
    names=['mktCap','size','mktCap_ff','size_ff']
    for name in names:
        df=pd.read_csv(os.path.join(SIZE_PATH,name+'.csv'),index_col=0)
        bps=cal_breakPoints(df,q)
        bps.to_csv(os.path.join(SIZE_PATH,'breakPoints_%s.csv'%name))
        count=count_groups(df,q)
        count.to_csv(os.path.join(SIZE_PATH,'count_%s.csv'%name))
        print(name)
    #TODO:In fact,the count is not exactly the number of stocks to calculate the weighted return
    #TODO:as some stocks will be deleted due to the missing of weights.

def portfolioEret(q=10):
    #TODO: ret winsorize? clip truncate?
    ret=read_df('stockRetM',freq='M')
    rf=read_df('rfM',freq='M')
    eret=ret.sub(rf['rf'],axis=0) # TODO: what's the unit of rf?

    def _wavg(df):
        if df.shape[0] > 0:
            d = df['ret']
            w = df['weight']
            return np.average(d, weights=w)
        else:
            return None

    def _eavg(df):
        if df.shape[0] > 0:
            return np.average(df['ret'])

    eret_wavg=pd.DataFrame(columns=['g' + str(i) for i in range(1, q + 1)])
    eret_eavg=pd.DataFrame(columns=['g' + str(i) for i in range(1, q + 1)])

    for name in ['mktCap','mktCap_ff']:
        cap=read_df(name,freq='M',repository=SIZE_PATH)
        # TODO: start fr
        # om 1996-01
        months=[m for m in cap.index.tolist() if m.year>=1996]
        for t in range(len(months)-1):
            #groups by using value of time t
            g=pd.qcut(cap.loc[months[t]],q,
                      labels=['g'+str(i) for i in range(1,q+1)])
            #returns of time t+1
            r=eret.loc[months[t+1]]
            #weight as market capital of time t
            w=cap.loc[months[t]]

            r.name = 'ret'
            w.name = 'weight'
            g.name = 'group'

            comb1 = pd.concat([r, w, g], axis=1)
            comb1 = comb1.dropna(axis=0, how='any')
            wavgs = comb1.groupby('group').apply(_wavg)
            eret_wavg.loc[months[t]] = wavgs

            comb2 = pd.concat([r, g], axis=1)
            comb2 = comb2.dropna(axis=0, how='any')
            eavgs = comb2.groupby('group').apply(_eavg)
            eret_eavg.loc[months[t]] = eavgs
            print(months[t])

        eret_wavg['g%s-g1' % q] = eret_wavg['g%s' % q] - eret_wavg['g1']
        eret_wavg.index.name = 't'
        eret_wavg['t+1'] = months[1:]
        cols = ['t+1'] + [col for col in eret_wavg.columns if col != 't+1']
        eret_wavg = eret_wavg.reindex(cols, axis=1)
        eret_wavg.to_csv(os.path.join(SIZE_PATH, 'eret_wavg_%s.csv'%name))

        eret_eavg['g%s-g1' % q] = eret_eavg['g%s' % q] - eret_eavg['g1']
        eret_eavg.index.name = 't'
        eret_eavg['t+1'] = months[1:]
        cols = ['t+1'] + [col for col in eret_eavg.columns if col != 't+1']
        eret_eavg = eret_eavg.reindex(cols, axis=1)
        eret_eavg.to_csv(os.path.join(SIZE_PATH, 'eret_eavg_%s.csv'%name))

mkt=read_df('mktRetM','M')

def _alpha(series):
    series.name=series.name.replace('-','_')#'-' should not appear in formula
    lags=5#TODO: setting for lags
    y=series.name
    x=mkt.columns[0]
    df=series.to_frame()
    df=pd.concat([df,mkt],axis=1)
    df=df.dropna()

    formula=y+' ~ '+x
    nw=assetPricing.newey_west(formula,df,lags=lags)
    return pd.Series(nw['Intercept'],index=['alpha','alpha_t'])

def _excess_ret(series):
    series.name=series.name.replace('-','_')#'-' should not appear in formula
    lags=5#TODO: setting for lags
    y=series.name
    df=series.to_frame()
    #TODO: add newey west function to assetPricing.py
    formula=y+' ~ 1'
    nw=assetPricing.newey_west(formula,df,lags)

    return pd.Series(nw['Intercept'],index=['excess return','excess return t'])

for name in ['eret_eavg_mktCap','eret_eavg_mktCap_ff',
             'eret_wavg_mktCap','eret_wavg_mktCap_ff']:
    port_eret=read_df(name,freq='M',repository=SIZE_PATH)
    port_eret = port_eret.set_index('t+1', drop=True)
    port_eret.index = pd.to_datetime(port_eret.index).to_period('M').to_timestamp('M')

    # table 8.4 part C
    alpha = port_eret.apply(_alpha)

    # table 8.4 part B
    excess_return = port_eret.apply(_excess_ret)

    # table 8.4 part A
    beta_portfolio = read_df('beta_portfolio_%s' % name, freq='M', repository=BETA_PATH)
    beta_avg = beta_portfolio.mean(axis=0)
    beta_avg[beta_avg.index[-1] + '-' + beta_avg.index[0]] = beta_avg.values[-1] - beta_avg.values[0]
    beta_avg.name = 'beta_avg'
    beta_avg = beta_avg.to_frame().T

    # table 8.4
    df = pd.concat([beta_avg, excess_return, alpha], axis=0)
    dfs.append(df)

# if __name__=='__main__':
#     cal_sizes()
#     summary()
#     correlation()
#     calculate_persistence()
#     get_percent_ratio()
#     breakPoints_and_countGroups()
#     portfolioEret()


