# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-28  10:09
# NAME:assetPricing-template.py

import numpy as np
import pandas as pd
import os
import statsmodels.formula.api as sm

from config import *
from zht.utils import assetPricing
from zht.utils.assetPricing import summary_statistics, cal_breakPoints, count_groups, famaMacBeth
from zht.utils.mathu import get_inter_index, reg, get_inter_frame, winsorize
from dout import read_df
from zht.utils.dfu import get_first_group


class Factor:
    def __init__(self, factorname, indicators, path):
        '''

        :param factorname:str,name of the factor,such size,beta value
        :param indicators:list, all kinds indicators for one factor,such as ['12M','1Y','3Y']
        :param path: where the indicators are stored
        '''
        self.factorname = factorname
        self.indicators = indicators
        self.path = path
        self.data=self.combine_indicators()

    def get_indicator(self, indicator):
        '''

        :param indicator:indicator of the indicator
        :return:
        '''
        return read_df(indicator, 'M', self.path)

    def combine_indicators(self):
        comb=pd.concat([self.get_indicator(indicator).stack() for indicator in self.indicators],
                         axis=1, keys=self.indicators)

        comb.index.names=['time','sid']
        return comb

class Dataset:
    def __init__(self, factors):
        '''

        :param factors: a list of Factor()
        '''
        self.factors=factors
        self.all_indicators={factor.factorname:factor.indicators for factor in self.factors}

    def combine_all_data(self):
        ret = read_df('stockRetM', freq='M')
        rf = read_df('rfM', freq='M')
        eret = ret.sub(rf['rf'], axis=0)
        e_ahead = eret.shift(-1)#regress on the eret of time t+1

        e_ahead = e_ahead.stack()
        e_ahead.index.names = ['time', 'sid']
        e_ahead.name = 'e_ahead'

        return pd.concat([factor.data for factor in self.factors]+[e_ahead],axis=1)

    def get_by_factor(self,factor):
        return factor.data

    def get_by_indicators(self,indicators):
        return self.combine_all_data()[indicators]



BETA = Factor('beta', BETA_NAMES, BETA_PATH)
SIZE = Factor('size', SIZE_NAMES, SIZE_PATH)
VALUE = Factor('value', VALUE_NAMES, VALUE_PATH)

dataset=Dataset([BETA,SIZE,VALUE])


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

mkt = read_df('mktRetM', 'M')

def _alpha(series):
    '''
    series should be single Index Series

    :param series:
    :return:
    '''
    series.name = series.name.replace('-', '_')  # '-' should not appear in formula
    lags = 5  # TODO: setting for lags
    y = series.name
    x = mkt.columns[0]
    df = series.to_frame()
    df = pd.concat([df, mkt], axis=1)
    df = df.dropna()

    formula = y + ' ~ ' + x
    nw = assetPricing.newey_west(formula, df, lags=lags)

    return nw['Intercept'].rename(index={'coef': 'alpha',
                                         't': 'alpha_t'})

def _excess_ret(series):
    series.name = series.name.replace('-', '_')  # '-' should not appear in formula
    lags = 5  # TODO: setting for lags
    y = series.name
    df = series.to_frame()
    formula = y + ' ~ 1'
    nw = assetPricing.newey_west(formula, df, lags)
    return nw['Intercept'].rename(index={'coef': 'excess return',
                                         't': 'excess return t'})




class Univariate:
    q=10

    def __init__(self,factor,path,names):
        self.factor=factor
        self.path=path
        self.names=names

    def summary(self):
        series=[]
        for name in self.names:
            df=read_df(name,freq='M',repository=self.path)
            s=summary_statistics(df,axis=1)
            s.to_csv(os.path.join(self.path,'summary_%s.csv'%name))
            series.append(s.mean())
        pd.concat(series,keys=self.names,axis=1).to_csv(os.path.join(self.path,'summary.csv'))

    def correlation_old(self):
        '''
        This table presents the time-series averages of the cross-sectional
        Pearson product-moment (below-diagonal entries) and Spearman rank
        (above-diagonal entries) correlations between pairs of variables
        .

        Returns:

        '''
        dfs=[read_df(name,freq='M',repository=self.path) for name in self.names]
        dfs=get_inter_frame(dfs)
        months=dfs[0].index.tolist()

        corrss = []
        corrps = []
        for month in months:
            corrdf = pd.DataFrame()
            for i in range(len(dfs)):
                corrdf[self.names[i]] = dfs[i].loc[month]

            corrs = assetPricing.corr(corrdf, 'spearman', winsorize=False)
            corrp = assetPricing.corr(corrdf, 'pearson', winsorize=True)

            corrss.append(corrs)
            corrps.append(corrp)

            print(month)
        s_concat = pd.concat(corrss)
        corrsAvg = s_concat.groupby(s_concat.index).mean()
        corrsAvg = corrsAvg.reindex(corrsAvg.columns)

        p_concat = pd.concat(corrps)
        corrpAvg = p_concat.groupby(p_concat.index).mean()
        corrpAvg = corrpAvg.reindex(corrpAvg.columns)

        corr1 = np.tril(corrpAvg.values, k=-1)
        corr2 = np.triu(corrsAvg.values, k=1)

        corr = pd.DataFrame(corr1 + corr2, index=corrpAvg.index, columns=corrpAvg.columns)
        np.fill_diagonal(corr.values, np.NaN)
        corr.to_csv(os.path.join(self.path, 'corr.csv'))
        corrpAvg.to_csv(os.path.join(self.path, 'corr_pearson.csv'))
        corrsAvg.to_csv(os.path.join(self.path, 'corr_spearman.csv'))

    def correlation(self, indicators=None):
        if not indicators:
            indicators=self.names

        comb=dataset.get_by_indicators(indicators)

        def _spearman(df):
            df=df.dropna()
            if df.shape[0]>10:#TODO:thresh to choose
                return assetPricing.corr(df,'spearman',winsorize=False)

        def _pearson(df):
            df=df.dropna()
            if df.shape[0]>10:
                return assetPricing.corr(df,'pearson',winsorize=True)

        corrs=comb.groupby('time').apply(_spearman)
        corrp=comb.groupby('time').apply(_pearson)

        corrsAvg=corrs.groupby(level=1).mean().reindex(index=indicators, columns=indicators)
        corrpAvg=corrp.groupby(level=1).mean().reindex(index=indicators, columns=indicators)

        corr1 = np.tril(corrpAvg.values, k=-1)
        corr2 = np.triu(corrsAvg.values, k=1)

        corr = pd.DataFrame(corr1 + corr2, index=corrpAvg.index, columns=corrpAvg.columns)
        np.fill_diagonal(corr.values, np.NaN)
        corr.to_csv(os.path.join(self.path, 'corr.csv'))
        corrpAvg.to_csv(os.path.join(self.path, 'corr_pearson.csv'))
        corrsAvg.to_csv(os.path.join(self.path, 'corr_spearman.csv'))

    def persistence(self):
        dfs=[read_df(name,freq='M',repository=self.path)
             for name in self.names]
        perdf = pd.DataFrame()
        for i in range(len(self.names)):
            per = assetPricing.persistence(dfs[i], offsets=[1, 3, 6, 12, 24, 36, 48, 60, 120])
            perdf[self.names[i]] = per
        perdf.to_csv(os.path.join(self.path,'persistence.csv'))

    def breakPoints_and_countGroups(self):
        for name in self.names:
            df=read_df(name,freq='M',repository=self.path)
            bps=cal_breakPoints(df,self.q)
            bps.to_csv(os.path.join(self.path,'breakPoints_%s.csv'%name))
            count=count_groups(df,self.q)
            count.to_csv(os.path.join(self.path,'count_%s.csv'%name))
        # TODO:In fact,the count is not exactly the number of stocks to calculate the weighted return
        # TODO:as some stocks will be deleted due to the missing of weights.

    def portfolioEret(self):
        ret=read_df('stockRetM',freq='M',repository=DATA_PATH)
        rf = read_df('rfM', freq='M')
        eret = ret.sub(rf['rf'], axis=0)
        mktCap = read_df('capM', freq='M', repository=DATA_PATH)

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

        for name in self.names:
            data=read_df(name,freq='M',repository=self.path)
            data,eret,mktCap=get_inter_index([data,eret,mktCap])
            months=[m for m in data.index if m.year>=1996]
            eret_wavg = pd.DataFrame(columns=['g' + str(i) for i in range(1, self.q + 1)])
            eret_eavg = pd.DataFrame(columns=['g' + str(i) for i in range(1, self.q + 1)])
            portfolio_value = pd.DataFrame(columns=['g' + str(i) for i in range(1, self.q + 1)])
            for t in range(len(months) - 1):
                #the time t is wrong,index denotes time t,but the return is that of time t+1
                #and in the following analysis,we should use the mktRet of time t+1 to calculate
                #capm alpha.So the time here is wrong!
                v = data.loc[months[t]]
                g = pd.qcut(v, self.q, labels=['g' + str(i) for i in range(1, self.q + 1)])
                r = eret.loc[months[t + 1]]
                if self.factor=='size':
                    #It should be noted that when MktCap is used as the sort variable,it is also used as the measure of
                    # market capitalization when weighting the portfolios.When mktCap_ff is used as the sort variable,
                    # we also use mktCap_ff to weight the portfolios.As page 159.
                    w=data.loc[months[t]]
                else:
                    w = mktCap.loc[months[t]]  # the weight is the market capitalization of time t

                v.name = self.factor
                r.name = 'ret'
                w.name = 'weight'
                g.name = 'group'

                comb = pd.concat([v, r, w, g], axis=1)
                comb = comb.dropna(axis=0)

                # value weighted
                wavgs = comb.groupby('group').apply(_wavg)
                eret_wavg.loc[months[t+1]] = wavgs#the time here denote the time of eret (t+1)

                # equal weighted
                eavgs = comb.groupby('group').apply(_eavg)
                eret_eavg.loc[months[t+1]] = eavgs

                # the average sort variable value
                asv = comb.groupby('group').apply(lambda x: x[self.factor].mean())
                portfolio_value.loc[months[t]] = asv#the time here denote time t,when we construct the portfolio
                print(name, months[t])

            eret_wavg['g%s-g1' % self.q] = eret_wavg['g%s' % self.q] - eret_wavg['g1']
            eret_wavg.index.name = 't'
            eret_wavg['t+1'] = months[1:]
            cols = ['t+1'] + [col for col in eret_wavg.columns if col != 't+1']
            eret_wavg = eret_wavg.reindex(cols, axis=1)
            eret_wavg.to_csv(os.path.join(self.path, 'eret_wavg_%s.csv' % name))

            eret_eavg['g%s-g1' % self.q] = eret_eavg['g%s' % self.q] - eret_eavg['g1']
            eret_eavg.index.name = 't'
            eret_eavg['t+1'] = months[1:]
            cols = ['t+1'] + [col for col in eret_eavg.columns if col != 't+1']
            eret_eavg = eret_eavg.reindex(cols, axis=1)
            eret_eavg.to_csv(os.path.join(self.path, 'eret_eavg_%s.csv' % name))

            portfolio_value.to_csv(os.path.join(self.path, '%s_portfolio_value_%s.csv' % (self.factor,name)))

    #TODO:do not use for loop,and replace it with apply groupby
    #TODO:store all the data in one sheet,it will reduce the time to read in data dramatically

    def univariate_portfolio_analysis(self):
        '''
        table 8.4

        :return:
        '''
        for weight in ['eavg', 'wavg']:
            dfs = []
            for name in self.names:
                port_eret = read_df('eret_%s_%s' % (weight, name), freq='M', repository=self.path)
                port_eret = port_eret.set_index('t+1', drop=True)
                port_eret.index = pd.to_datetime(port_eret.index).to_period('M').to_timestamp('M')

                # table 8.4 part C
                alpha = port_eret.apply(_alpha)

                # table 8.4 part B
                excess_return = port_eret.apply(_excess_ret)

                # table 8.4 part A
                portfolio_value = read_df('%s_portfolio_value_%s' % (self.factor,name), freq='M', repository=self.path)
                factor_avg = portfolio_value.mean(axis=0)
                factor_avg[factor_avg.index[-1] + '-' + factor_avg.index[0]] = factor_avg.values[-1] - factor_avg.values[0]
                factor_avg.name = 'factor_avg'
                factor_avg = factor_avg.to_frame().T

                # table 8.4
                df = pd.concat([factor_avg, excess_return, alpha], axis=0)
                dfs.append(df)

            com = pd.concat(dfs, keys=self.names)
            com.to_csv(os.path.join(self.path, 'univariate portfolio analysis_%s.csv' % weight))

    def fm_analysis(self):
        '''
        as table8.6

        :return:
        '''
        ret = read_df('stockRetM', freq='M')
        rf = read_df('rfM', freq='M')
        eret = ret.sub(rf['rf'], axis=0)
        e_ahead = eret.shift(-1)  # The dependent variable is one-month-ahead excesss stock return
        #TODO: winsorize ratio?
        e_ahead = winsorize(e_ahead, limits=(0.01, 0.01),axis=0)  # winsorize the independent variable at 0.5% level on a monthly basis
        e_ahead = e_ahead.stack()
        e_ahead.name = 'y'

        data = []
        for name in self.names:
            factor = read_df(name, freq='M', repository=self.path)
            factor = factor.stack()
            factor.name = 'x'
            df = pd.concat([factor, e_ahead], axis=1)
            df.index.names = ['month', 'sid']
            df = df.dropna(axis=0)
            df = df.groupby(level='month').filter(
                lambda x: x.shape[0] > 50)  # get months with samples more than 50 for proper regression
            df = df.reset_index()

            formula = 'y ~ x'
            r, adj_r2, n = famaMacBeth(formula, 'month', df, lags=5)
            data.append([r.loc['x', 'coef'], r.loc['x', 'tvalue'],
                         r.loc['Intercept', 'coef'], r.loc['Intercept', 'tvalue'],
                         adj_r2, n])
            print(name)
        result = pd.DataFrame(data, index=self.names,
                              columns=['slope', 't', 'Intercept', 'Intercept_t', 'adj_r2', 'n']).T
        result.to_csv(os.path.join(self.path, 'fama macbeth regression analysis.csv'))

    # TODO: truncate the samples

    def run(self):
        self.summary()
        self.correlation()
        self.persistence()
        self.breakPoints_and_countGroups()
        self.portfolioEret()
        self.univariate_portfolio_analysis()
        self.fm_analysis()

#TODO:the unit should be % for returns as the book
#TODO: truncate the samples


class Beta(Univariate):
    def __init__(self):
        super().__init__('beta',BETA_PATH,BETA_NAMES)

class Size(Univariate):
    #TODO:chooose different breakpoints like table 9.5
    def __init__(self):
        super().__init__('size',SIZE_PATH,SIZE_NAMES)

    def get_percent_ratio(self):
        df=read_df('mktCap',freq='M',repository=self.path)

        def _get_ratio(s):
            ratios = [1, 5, 10, 25]
            return pd.Series([s.nlargest(r).sum() / s.sum() for r in ratios],
                             index=ratios)

        r = df.apply(_get_ratio, axis=1)
        r.index = r.index.to_datetime().to_period('M')
        fig = r[40:].plot().get_figure()
        fig.savefig(os.path.join(self.path, 'percent of market value.png'))

    def run(self):
        super().run()
        self.get_percent_ratio()

class Value(Univariate):
    def __init__(self):
        super().__init__('value',VALUE_PATH,VALUE_NAMES)

    def correlation(self):
        indicators=['bm', 'logbm', '12M', 'size']
        super().correlation(indicators)

    def run(self):
        super().run()



class Bivariate_old:
    #TODO: table 10.5
    q=5

    def __init__(self,proj_path,factor1,factor2,var1name,var2name,var1path,var2path):
        self.proj_path = proj_path
        self.factor1 = factor1
        self.factor2 = factor2
        self.var1name = var1name
        self.var2name = var2name
        self.var1path = var1path
        self.var2path = var2path

    def _get_independent_gid(self):
        # TODO: add the method of ratios such as [0.3,0.7]
        var1 = read_df(self.var1name, freq='M', repository=self.var1path)
        var2 = read_df(self.var2name, freq='M', repository=self.var2path)

        comb=pd.concat([var1.stack(),var2.stack()],axis=1,keys=['var1','var2'])
        comb=comb.dropna()
        comb.index.names=['time','sid']

        #TODO:different with dependent variable
        comb['g1']=comb.groupby('time',group_keys=False).apply(
            lambda df:pd.qcut(df['var1'],self.q,
                              labels=[self.factor1+str(i) for i in range(1,self.q+1)])
        )

        comb['g2']=comb.groupby('time',group_keys=False).apply(
            lambda df:pd.qcut(df['var2'],self.q,
                              labels=[self.factor2+str(i) for i in range(1,self.q+1)])
        )

        return comb[['g1','g2']]

    def _get_dependent_gid(self):
        #TODO: change the order of the two factors
        var1 = read_df(self.var1name, freq='M', repository=self.var1path)
        var2 = read_df(self.var2name, freq='M', repository=self.var2path)

        comb=pd.concat([var1.stack(),var2.stack()],axis=1,keys=['var1','var2'])
        comb=comb.dropna()
        comb.index.names=['time','sid']

        #use group_keys=False avoid the duplicate index
        comb['g1']=comb.groupby('time',group_keys=False).apply(
            lambda df:pd.qcut(df['var1'],self.q,
                              labels=[self.factor1+str(i) for i in range(1,self.q+1)])
        )

        comb['g2']=comb.groupby(['time','g1'],group_keys=False).apply(
            lambda df:pd.qcut(df['var2'],self.q,
                              labels=[self.factor2+str(i) for i in range(1,self.q+1)])
        )

        return comb[['g1','g2']]

    def _combine_data(self,gid):
        gid=gid.reset_index('time')
        gid['time']=gid.groupby('sid')['time'].shift(-1)#The time denotes t+1
        gid=gid.reset_index()
        gid=gid.set_index(['time','sid'])

        ret = read_df('stockRetM', freq='M', repository=DATA_PATH)
        rf = read_df('rfM', freq='M')
        eret = ret.sub(rf['rf'], axis=0)
        mktCap = read_df('capM', freq='M', repository=DATA_PATH)

        eret=eret.stack()
        eret.index.names=['time','sid']
        eret.name='eret'

        mktCap=mktCap.stack()
        mktCap.index.names=['time','sid']
        mktCap.name='mktCap'

        comb=pd.concat([gid,eret,mktCap],axis=1)
        comb=comb.dropna()
        return comb

    def _get_eret(self,comb):
        group_eavg_ts = comb.groupby(['g1', 'g2', 'time'])['eret'].mean()
        group_wavg_ts = comb.groupby(['g1', 'g2', 'time']).apply(
            lambda df: _wavg(df.rename(columns={'eret': 'ret', 'mktCap': 'weight'})))
        return group_eavg_ts,group_wavg_ts

    def _independent_portfolio_analysis(self,group_ts):
        '''
        table 9.9

        :param group_ts:
        :return:
        '''
        #part A
        _a=group_ts.groupby(['g1','g2']).mean()
        _a=_a.unstack().T

        table=_a.copy()
        table.index=table.index.astype(str)
        table.columns=table.columns.astype(str)

        #part B
        _b1=group_ts.groupby(['time','g1']).mean().groupby('g1').mean()
        _b2=group_ts.groupby(['time','g2']).mean().groupby('g2').mean()

        table.loc[self.factor2+' avg']=_b1
        table[self.factor1+' avg']=_b2

        #part C
        #TODO:s[-1]-s[0] is not so rigorous,use labels to select the big and the small
        c1_data=group_ts.groupby(['g1','time']).apply(lambda s:s[-1]-s[0])
        _c1=c1_data.groupby('g1').apply(_excess_ret).unstack().T
        _c1.index=[self.factor2+str(self.q)+'-1',self.factor2+str(self.q)+'-1 t']
        table=pd.concat([table,_c1],axis=0)

        c2_data=group_ts.groupby(['g2','time']).apply(lambda s:s[-1]-s[0])
        _c2=c2_data.groupby('g2').apply(_excess_ret).unstack()
        _c2.columns=[self.factor1+str(self.q)+'-1',self.factor1+str(self.q)+'-1 t']
        table=pd.concat([table,_c2],axis=1)

        #part D
        _d1=c1_data.groupby('g1').apply(lambda x:_alpha(x.reset_index('g1',drop=True))).unstack().T
        _d1.index=[self.factor2+str(self.q)+'-1 capm alpha',self.factor2+str(self.q)+'-1 capm alpha t']
        table=pd.concat([table,_d1],axis=0)

        _d2=c2_data.groupby('g2').apply(lambda x:_alpha(x.reset_index('g2',drop=True))).unstack()
        _d2.columns=[self.factor1+str(self.q)+'-1 capm alpha',self.factor1+str(self.q)+'-1 capm alpha t']
        table=pd.concat([table,_d2],axis=1)

        #part E
        e1_data=group_ts.groupby(['time','g1']).mean().groupby('time').apply(lambda s:s[-1]-s[0])
        e1_data.name='eret'
        _e1=_excess_ret(e1_data)

        e2_data=group_ts.groupby(['time','g2']).mean().groupby('time').apply(lambda s:s[-1]-s[0])
        e2_data.name='eret'
        _e2=_excess_ret(e2_data)

        table.loc[self.factor2+' avg',[self.factor1+str(self.q)+'-1',self.factor1+str(self.q)+'-1 t']]=_e1.values
        table.loc[[self.factor2+str(self.q)+'-1',self.factor2+str(self.q)+'-1 t'],self.factor1+' avg']=_e2.values

        #part F
        _f1=_alpha(e1_data)
        _f2=_alpha(e2_data)

        table.loc[self.factor2+' avg',[self.factor1+str(self.q)+'-1 capm alpha',self.factor1+str(self.q)+'-1 capm alpha t']]=_f1.values
        table.loc[[self.factor2+str(self.q)+'-1 capm alpha',self.factor2+str(self.q)+'-1 capm alpha t'],self.factor1+' avg']=_f2.values

        newcolumns = [self.factor1 + str(i) for i in range(1, self.q + 1)] + \
                   [self.factor1 + ' avg', self.factor1 + str(self.q) + '-1', self.factor1 + str(self.q) + '-1 t',
                    self.factor1 + str(self.q) + '-1 capm alpha', self.factor1 + str(self.q) + '-1 capm alpha t']

        newindex = [self.factor2 + str(i) for i in range(1, self.q + 1)] + \
                     [self.factor2 + ' avg', self.factor2 + str(self.q) + '-1', self.factor2 + str(self.q) + '-1 t',
                      self.factor2 + str(self.q) + '-1 capm alpha', self.factor2 + str(self.q) + '-1 capm alpha t']

        # reindex the table
        table = table.reindex(index=newindex, columns=newcolumns)
        return table

    def _dependent_portfolio_analysis(self,group_ts):
        # Table 9.6

        #part A
        _a=group_ts.groupby(['g1','g2']).mean()
        _a=_a.unstack().T
        table=_a.copy()

        #part B
        _b=group_ts.groupby(['time','g2']).mean().groupby('g2').mean()
        table.index=table.index.astype(str)#convert categorical index to str index
        table.columns=table.columns.astype(str)
        table[self.factor1+' avg']=_b.values

        #part C
        #TODO:s[-1]-s[0] is not so rigorous,use labels to select the big and the small
        c_data=group_ts.groupby(['g1','time']).apply(lambda s:s[-1]-s[0])
        _c=c_data.groupby('g1').apply(_excess_ret).unstack().T
        _c.index=[self.factor2+str(self.q)+'-1',self.factor2+str(self.q)+'-1 t']
        table=pd.concat([table,_c],axis=0)

        #part D
        _d=c_data.groupby('g1').apply(lambda x:_alpha(x.reset_index('g1',drop=True))).unstack().T
        _d.index=[self.factor2+str(self.q)+'-1 capm alpha',self.factor2+str(self.q)+'-1 capm alpha t']
        table=pd.concat([table,_d],axis=0)

        #part E
        e_data=group_ts.groupby(['time','g2']).mean().groupby('time').apply(lambda s:s[-1]-s[0])
        e_data.name='eret'
        _e=_excess_ret(e_data)
        table.loc[[self.factor2+str(self.q)+'-1',self.factor2+str(self.q)+'-1 t'],self.factor1+' avg']=_e.values

        #part F
        _f=_alpha(e_data)
        table.loc[[self.factor2+str(self.q)+'-1 capm alpha',self.factor2+str(self.q)+'-1 capm alpha t'],self.factor1+' avg']=_f.values

        newColumns=[self.factor1+str(i) for i in range(1,self.q+1)]+[self.factor1+' avg']
        table=table.reindex(columns=newColumns)
        return table

    def independent_portfolio_analysis(self):
        gid=self._get_independent_gid()
        comb=self._combine_data(gid)
        group_eavg_ts, group_wavg_ts = self._get_eret(comb)

        table_eavg = self._independent_portfolio_analysis(group_eavg_ts)
        table_wavg = self._independent_portfolio_analysis(group_wavg_ts)
        table_eavg.to_csv(os.path.join(self.proj_path,
            'bivariate independent-sort portfolio analysis_equal weighted_%s_%s.csv'%(self.factor1,self.factor2)))
        table_wavg.to_csv(os.path.join(self.proj_path,
            'bivariate independent-sort portfolio analysis_value weighted_%s_%s.csv'%(self.factor1,self.factor2)))

    def dependent_portfolio_analysis(self):
        gid=self._get_dependent_gid()
        comb=self._combine_data(gid)
        group_eavg_ts, group_wavg_ts = self._get_eret(comb)

        table_eavg = self._dependent_portfolio_analysis(group_eavg_ts)
        table_wavg = self._dependent_portfolio_analysis(group_wavg_ts)
        table_eavg.to_csv(os.path.join(self.proj_path,
            'bivariate dependent-sort portfolio analysis_equal weighted_%s_%s.csv'%(self.factor1,self.factor2)))
        table_wavg.to_csv(os.path.join(self.proj_path,
            'bivariate dependent-sort portfolio analysis_value weighted_%s_%s.csv'%(self.factor1,self.factor2)))

    def _comb_df_for_fm(self):
        size = read_df('size', 'M', SIZE_PATH)
        size_ff = read_df('size_ff', 'M', SIZE_PATH)
        beta = read_df('12M', 'M', BETA_PATH)

        size = size.stack()
        size.index.names = ['time', 'sid']
        size.name = 'size'

        size_ff = size_ff.stack()
        size_ff.index.names = ['time', 'sid']
        size_ff.name = 'size_ff'

        beta = beta.stack()
        beta.index.names = ['time', 'sid']
        beta.name = 'beta'

        ret = read_df('stockRetM', freq='M')
        rf = read_df('rfM', freq='M')
        eret = ret.sub(rf['rf'], axis=0)
        e_ahead = eret.shift(-1)

        e_ahead = e_ahead.stack()
        e_ahead.index.names = ['time', 'sid']
        e_ahead.name = 'e_ahead'

        comb = pd.concat([size, size_ff, beta, e_ahead], axis=1)
        return comb

    def fm_analysis(self):
        '''
        table 9.10

        :param self:
        :return:
        '''
        comb=self._comb_df_for_fm()
        comb=comb.reset_index()


        formula1='e_ahead ~ size'
        df1=comb[['time','e_ahead','size']].dropna()

        formula2='e_ahead ~ size + beta'
        df2=comb[['time','e_ahead','size','beta']].dropna()

        formula3='e_ahead ~ size_ff'
        df3=comb[['time','e_ahead','size_ff']].dropna()

        formula4='e_ahead ~ size_ff + beta'
        df4=comb[['time','e_ahead','size_ff','beta']].dropna()

        r1,adj_r2_1,n1=famaMacBeth(formula1,'time',df1,lags=5)
        r2,adj_r2_2,n2=famaMacBeth(formula2,'time',df2,lags=5)
        r3,adj_r2_3,n3=famaMacBeth(formula3,'time',df3,lags=5)
        r4,adj_r2_4,n4=famaMacBeth(formula4,'time',df4,lags=5)

        stk1=r1[['coef','tvalue']].stack()
        stk1.index=stk1.index.map('{0[0]} {0[1]}'.format)
        stk1['adj_r2'] = adj_r2_1
        stk1['n'] = n1

        stk2=r2[['coef','tvalue']].stack()
        stk2.index=stk2.index.map('{0[0]} {0[1]}'.format)
        stk2['adj_r2'] = adj_r2_2
        stk2['n'] = n2

        stk3=r3[['coef','tvalue']].stack()
        stk3.index=stk3.index.map('{0[0]} {0[1]}'.format)
        stk3['adj_r2'] = adj_r2_3
        stk3['n'] = n3

        stk4=r4[['coef','tvalue']].stack()
        stk4.index=stk4.index.map('{0[0]} {0[1]}'.format)
        stk4['adj_r2'] = adj_r2_4
        stk4['n'] = n4

        table=pd.concat([stk1,stk2,stk3,stk4],axis=1,
                  keys=['formula1','formula2','formula3','formula4'])

        newIndex=['size coef','size tvalue','size_ff coef','size_ff tvalue',
                  'beta coef','beta tvalue','Intercept coef','Intercept tvalue',
                  'adj_r2','n']

        table=table.reindex(index=newIndex)

        table.to_csv(os.path.join(os.path.join(SIZE_PATH,'fama macbeth regression analysis')))

class Bivariate:
    q=5

    def __init__(self,indicators,factornames,proj_path):
        '''
        :param indicators:list,indicators to analyse,do not need to include eret.
        :param factornames:list the name of the factors to analyse,such as ['size','beta']
        :param proj_path:
        '''
        self.indicators=indicators
        self.factornames=factornames
        self.proj_path=proj_path

    def _get_independent_gid(self):
        # TODO: add the method of ratios such as [0.3,0.7]
        comb=dataset.get_by_indicators(self.indicators)
        comb=comb.dropna()
        comb['g1']=comb.groupby('time',group_keys=False).apply(
            lambda df:pd.qcut(df[self.indicators[0]],self.q,
                              labels=[self.factornames[0]+str(i) for i in range(1,self.q+1)])
        )

        comb['g2']=comb.groupby('time',group_keys=False).apply(
            lambda df:pd.qcut(df[self.indicators[1]],self.q,
                              labels=[self.factornames[1]+str(i) for i in range(1,self.q+1)])
        )

        return comb[['g1','g2']]

    def _get_dependent_gid(self,indicators,factornames):
        #TODO: change the order of the two factors
        #use group_keys=False avoid the duplicate index
        comb=dataset.get_by_indicators(indicators)
        comb=comb.dropna()

        comb['g1']=comb.groupby('time',group_keys=False).apply(
            lambda df:pd.qcut(df[indicators[0]],self.q,
                              labels=[factornames[0]+str(i) for i in range(1,self.q+1)])
        )

        comb['g2']=comb.groupby(['time','g1'],group_keys=False).apply(
            lambda df:pd.qcut(df[indicators[1]],self.q,
                              labels=[factornames[1]+str(i) for i in range(1,self.q+1)])
        )

        return comb[['g1','g2']]

    def _combine_data(self,gid):
        gid=gid.reset_index('time')
        gid['time']=gid.groupby('sid')['time'].shift(-1)#The time denotes t+1
        gid=gid.reset_index()
        gid=gid.set_index(['time','sid'])

        ret = read_df('stockRetM', freq='M', repository=DATA_PATH)
        rf = read_df('rfM', freq='M')
        eret = ret.sub(rf['rf'], axis=0)
        mktCap = read_df('capM', freq='M', repository=DATA_PATH)

        eret=eret.stack()
        eret.index.names=['time','sid']
        eret.name='eret'

        mktCap=mktCap.stack()
        mktCap.index.names=['time','sid']
        mktCap.name='mktCap'

        comb=pd.concat([gid,eret,mktCap],axis=1)
        comb=comb.dropna()
        return comb

    def _get_eret(self,comb):
        group_eavg_ts = comb.groupby(['g1', 'g2', 'time'])['eret'].mean()
        group_wavg_ts = comb.groupby(['g1', 'g2', 'time']).apply(
            lambda df: _wavg(df.rename(columns={'eret': 'ret', 'mktCap': 'weight'})))
        return group_eavg_ts,group_wavg_ts

    def _independent_portfolio_analysis(self,group_ts):
        '''
        table 9.9

        :param group_ts:
        :return:
        '''
        #part A
        _a=group_ts.groupby(['g1','g2']).mean()
        _a=_a.unstack().T

        table=_a.copy()
        table.index=table.index.astype(str)
        table.columns=table.columns.astype(str)

        #part B
        _b1=group_ts.groupby(['time','g1']).mean().groupby('g1').mean()
        _b2=group_ts.groupby(['time','g2']).mean().groupby('g2').mean()

        table.loc[self.indicators[1]+' avg']=_b1
        table[self.indicators[0]+' avg']=_b2

        #part C
        #TODO:s[-1]-s[0] is not so rigorous,use labels to select the big and the small
        c1_data=group_ts.groupby(['g1','time']).apply(lambda s:s[-1]-s[0])
        _c1=c1_data.groupby('g1').apply(_excess_ret).unstack().T
        _c1.index=[self.indicators[1]+str(self.q)+'-1',self.indicators[1]+str(self.q)+'-1 t']
        table=pd.concat([table,_c1],axis=0)

        c2_data=group_ts.groupby(['g2','time']).apply(lambda s:s[-1]-s[0])
        _c2=c2_data.groupby('g2').apply(_excess_ret).unstack()
        _c2.columns=[self.indicators[0]+str(self.q)+'-1',self.indicators[0]+str(self.q)+'-1 t']
        table=pd.concat([table,_c2],axis=1)

        #part D
        _d1=c1_data.groupby('g1').apply(lambda x:_alpha(x.reset_index('g1',drop=True))).unstack().T
        _d1.index=[self.indicators[1]+str(self.q)+'-1 capm alpha',self.indicators[1]+str(self.q)+'-1 capm alpha t']
        table=pd.concat([table,_d1],axis=0)

        _d2=c2_data.groupby('g2').apply(lambda x:_alpha(x.reset_index('g2',drop=True))).unstack()
        _d2.columns=[self.indicators[0]+str(self.q)+'-1 capm alpha',self.indicators[0]+str(self.q)+'-1 capm alpha t']
        table=pd.concat([table,_d2],axis=1)

        #part E
        e1_data=group_ts.groupby(['time','g1']).mean().groupby('time').apply(lambda s:s[-1]-s[0])
        e1_data.name='eret'
        _e1=_excess_ret(e1_data)

        e2_data=group_ts.groupby(['time','g2']).mean().groupby('time').apply(lambda s:s[-1]-s[0])
        e2_data.name='eret'
        _e2=_excess_ret(e2_data)

        table.loc[self.indicators[1]+' avg',[self.indicators[0]+str(self.q)+'-1',self.indicators[0]+str(self.q)+'-1 t']]=_e1.values
        table.loc[[self.indicators[1]+str(self.q)+'-1',self.indicators[1]+str(self.q)+'-1 t'],self.indicators[0]+' avg']=_e2.values

        #part F
        _f1=_alpha(e1_data)
        _f2=_alpha(e2_data)

        table.loc[self.indicators[1]+' avg',[self.indicators[0]+str(self.q)+'-1 capm alpha',self.indicators[0]+str(self.q)+'-1 capm alpha t']]=_f1.values
        table.loc[[self.indicators[1]+str(self.q)+'-1 capm alpha',self.indicators[1]+str(self.q)+'-1 capm alpha t'],self.indicators[0]+' avg']=_f2.values

        newcolumns = [self.indicators[0] + str(i) for i in range(1, self.q + 1)] + \
                   [self.indicators[0] + ' avg', self.indicators[0] + str(self.q) + '-1', self.indicators[0] + str(self.q) + '-1 t',
                    self.indicators[0] + str(self.q) + '-1 capm alpha', self.indicators[0] + str(self.q) + '-1 capm alpha t']

        newindex = [self.indicators[1] + str(i) for i in range(1, self.q + 1)] + \
                     [self.indicators[1] + ' avg', self.indicators[1] + str(self.q) + '-1', self.indicators[1] + str(self.q) + '-1 t',
                      self.indicators[1] + str(self.q) + '-1 capm alpha', self.indicators[1] + str(self.q) + '-1 capm alpha t']

        # reindex the table
        table = table.reindex(index=newindex, columns=newcolumns)
        return table

    def _dependent_portfolio_analysis(self,group_ts):
        # Table 9.6

        #part A
        _a=group_ts.groupby(['g1','g2']).mean()
        _a=_a.unstack().T
        table=_a.copy()

        #part B
        _b=group_ts.groupby(['time','g2']).mean().groupby('g2').mean()
        table.index=table.index.astype(str)#convert categorical index to str index
        table.columns=table.columns.astype(str)
        table[self.indicators[0]+' avg']=_b.values

        #part C
        #TODO:s[-1]-s[0] is not so rigorous,use labels to select the big and the small
        c_data=group_ts.groupby(['g1','time']).apply(lambda s:s[-1]-s[0])
        _c=c_data.groupby('g1').apply(_excess_ret).unstack().T
        _c.index=[self.indicators[1]+str(self.q)+'-1',self.indicators[1]+str(self.q)+'-1 t']
        table=pd.concat([table,_c],axis=0)

        #part D
        _d=c_data.groupby('g1').apply(lambda x:_alpha(x.reset_index('g1',drop=True))).unstack().T
        _d.index=[self.indicators[1]+str(self.q)+'-1 capm alpha',self.indicators[1]+str(self.q)+'-1 capm alpha t']
        table=pd.concat([table,_d],axis=0)

        #part E
        e_data=group_ts.groupby(['time','g2']).mean().groupby('time').apply(lambda s:s[-1]-s[0])
        e_data.name='eret'
        _e=_excess_ret(e_data)
        table.loc[[self.indicators[1]+str(self.q)+'-1',self.indicators[1]+str(self.q)+'-1 t'],self.indicators[0]+' avg']=_e.values

        #part F
        _f=_alpha(e_data)
        table.loc[[self.indicators[1]+str(self.q)+'-1 capm alpha',self.indicators[1]+str(self.q)+'-1 capm alpha t'],self.indicators[0]+' avg']=_f.values

        newColumns=[self.indicators[0]+str(i) for i in range(1,self.q+1)]+[self.indicators[0]+' avg']
        table=table.reindex(columns=newColumns)
        return table

    def independent_portfolio_analysis(self):
        gid=self._get_independent_gid()
        comb=self._combine_data(gid)
        group_eavg_ts, group_wavg_ts = self._get_eret(comb)

        table_eavg = self._independent_portfolio_analysis(group_eavg_ts)
        table_wavg = self._independent_portfolio_analysis(group_wavg_ts)
        table_eavg.to_csv(os.path.join(self.proj_path,
            'bivariate independent-sort portfolio analysis_equal weighted_%s_%s.csv'%(self.indicators[0],self.indicators[1])))
        table_wavg.to_csv(os.path.join(self.proj_path,
            'bivariate independent-sort portfolio analysis_value weighted_%s_%s.csv'%(self.indicators[0],self.indicators[1])))

    def dependent_portfolio_analysis(self):
        def _f(indicators,factornames):
            gid=self._get_dependent_gid(indicators,factornames)

            comb=self._combine_data(gid)
            group_eavg_ts, group_wavg_ts = self._get_eret(comb)

            table_eavg = self._dependent_portfolio_analysis(group_eavg_ts)
            table_wavg = self._dependent_portfolio_analysis(group_wavg_ts)
            table_eavg.to_csv(os.path.join(self.proj_path,
                'bivariate dependent-sort portfolio analysis_equal weighted_%s_%s.csv'%(factornames[0],factornames[1])))
            table_wavg.to_csv(os.path.join(self.proj_path,
                'bivariate dependent-sort portfolio analysis_value weighted_%s_%s.csv'%(factornames[0],factornames[1])))

        _f(self.indicators,self.factornames)
        _f(self.indicators[::-1],self.factornames[::-1])

    def _fm(self,ll_indeVars):
        '''

        :param ll_indeVars: list of list,the inside list contains all
            the indepedent variables to construct a regress equation
        :return:
        '''
        indicators=list(set(var for l_indeVars in ll_indeVars for var in l_indeVars))+['e_ahead']
        comb=dataset.get_by_indicators(indicators)
        comb=comb.reset_index()

        stks=[]
        for l_indeVars in ll_indeVars:
            formula='e_ahead ~ '+' + '.join(l_indeVars)#TODO: 12M
            df=comb[l_indeVars+['time','e_ahead']].dropna()
            #TODO:lags?
            r,adj_r2,n=famaMacBeth(formula,'time',df,lags=5)
            stk=r[['coef','tvalue']].stack()
            stk.index=stk.index.map('{0[0]} {0[1]}'.format)
            stk['adj_r2']=adj_r2
            stk['n']=n
            stks.append(stk)
        table=pd.concat(stks,axis=1,keys=range(1,len(ll_indeVars)+1))

        newIndex=[var+' '+suffix for var in indicators for suffix in ['coef','tvalue']]+ \
            ['Intercept coef','Intercept tvalue','adj_r2','n']

        table=table.reindex(index=newIndex)

        table.to_csv(os.path.join(os.path.join(self.proj_path,'fama macbeth regression analysis')))


    def _comb_df_for_fm(self):
        size = read_df('size', 'M', SIZE_PATH)
        size_ff = read_df('size_ff', 'M', SIZE_PATH)
        beta = read_df('12M', 'M', BETA_PATH)

        size = size.stack()
        size.index.names = ['time', 'sid']
        size.name = 'size'

        size_ff = size_ff.stack()
        size_ff.index.names = ['time', 'sid']
        size_ff.name = 'size_ff'

        beta = beta.stack()
        beta.index.names = ['time', 'sid']
        beta.name = 'beta'

        ret = read_df('stockRetM', freq='M')
        rf = read_df('rfM', freq='M')
        eret = ret.sub(rf['rf'], axis=0)
        e_ahead = eret.shift(-1)#regress on the eret of time t+1

        e_ahead = e_ahead.stack()
        e_ahead.index.names = ['time', 'sid']
        e_ahead.name = 'e_ahead'

        comb = pd.concat([size, size_ff, beta, e_ahead], axis=1)
        return comb

    def fm_analysis(self):
        '''
        table 9.10

        :param self:
        :return:
        '''
        comb=self._comb_df_for_fm()
        comb=comb.reset_index()


        formula1='e_ahead ~ size'
        df1=comb[['time','e_ahead','size']].dropna()

        formula2='e_ahead ~ size + beta'
        df2=comb[['time','e_ahead','size','beta']].dropna()

        formula3='e_ahead ~ size_ff'
        df3=comb[['time','e_ahead','size_ff']].dropna()

        formula4='e_ahead ~ size_ff + beta'
        df4=comb[['time','e_ahead','size_ff','beta']].dropna()

        r1,adj_r2_1,n1=famaMacBeth(formula1,'time',df1,lags=5)
        r2,adj_r2_2,n2=famaMacBeth(formula2,'time',df2,lags=5)
        r3,adj_r2_3,n3=famaMacBeth(formula3,'time',df3,lags=5)
        r4,adj_r2_4,n4=famaMacBeth(formula4,'time',df4,lags=5)

        stk1=r1[['coef','tvalue']].stack()
        stk1.index=stk1.index.map('{0[0]} {0[1]}'.format)
        stk1['adj_r2'] = adj_r2_1
        stk1['n'] = n1

        stk2=r2[['coef','tvalue']].stack()
        stk2.index=stk2.index.map('{0[0]} {0[1]}'.format)
        stk2['adj_r2'] = adj_r2_2
        stk2['n'] = n2

        stk3=r3[['coef','tvalue']].stack()
        stk3.index=stk3.index.map('{0[0]} {0[1]}'.format)
        stk3['adj_r2'] = adj_r2_3
        stk3['n'] = n3

        stk4=r4[['coef','tvalue']].stack()
        stk4.index=stk4.index.map('{0[0]} {0[1]}'.format)
        stk4['adj_r2'] = adj_r2_4
        stk4['n'] = n4

        table=pd.concat([stk1,stk2,stk3,stk4],axis=1,
                  keys=['formula1','formula2','formula3','formula4'])

        newIndex=['size coef','size tvalue','size_ff coef','size_ff tvalue',
                  'beta coef','beta tvalue','Intercept coef','Intercept tvalue',
                  'adj_r2','n']

        table=table.reindex(index=newIndex)

        table.to_csv(os.path.join(os.path.join(SIZE_PATH,'fama macbeth regression analysis')))



def test_bivariate():
    factor1 = 'beta'
    factor2 = 'size'
    # use one year worth of daily return data to calculate beta as stated in page 143
    var1name = '12M'
    # use mktCap as the measure of market capitalization as stated in page 162
    var2name = 'mktCap'


class Size_mkt_bivariate(Bivariate):
    def __init__(self):
        indicators = ['12M', 'mktCap']
        factornames=['beta','size']
        proj_path = r'D:\zht\database\quantDb\researchTopics\assetPricingNew\tmp'
        super().__init__(indicators,factornames,proj_path)

    def fm(self):
        ll_indeVars = [['size'], ['size', '12M'], ['size_ff'], ['size_ff', '12M']]
        super()._fm(ll_indeVars)

    def run(self):
        self.independent_portfolio_analysis()
        self.dependent_portfolio_analysis()
        self.fm()


Size_mkt_bivariate().run()




#TODO: use different breakpoints as discussed in the book

# if __name__=='__main__':
    # Value().run()

# if __name__=='__main__':
#     Beta().run()
#     Size().run()

#TODO:document the code
#TODO:check the results carefully to detect errors
#TODO:notice that due to Chinese Spring festive there may be no data in some months especially February
    # Value().run()

