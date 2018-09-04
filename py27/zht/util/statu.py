#-*-coding: utf-8 -*-
#author:tyhj
#statu.py 2017/8/13 10:26
import numpy as np
import scipy

import pandas as pd
import os
from pandas.io.formats.format import format_percentiles
import statsmodels.formula.api as sm


from zht.util import pandasu



def GRS_test(factor,resid,alpha):
    '''
        returns the GRS test statistic and its corresponding p-value proposed in
    Gibbons,Ross,Shanken (1989),to test the hypothesis:alpha1=alpha2=...=alphaN=0.
    That is if the alphas from time series Regression on N Test Assets are
    cummulatively zero.

    Args:
        factor:TxL Matrix of factor returns (the "Matrix" means numpy.matrixlib.defmatrix.matrix)
        resid: TxN Matrix of residuals from TS-regression
        alpha: Nx1 Matrix of intercepts from TS-regression

    details:
        N:the number of assets (or the number of regressions)
        T:the number of the observations
        L:the number of the factors

    Returns:
        GRS[0,0]:1x1 scalar of GRS Test-value
        pvalue[0,0]:1x1 scalar of P-value from an F-Distribution

    '''
    T, N = resid.shape
    L = factor.shape[1]

    mu_mean = np.mat(factor.mean(0)).reshape(L,1)  # Lx1 mean excess factor returns
    cov_e=np.cov(resid.T).reshape(N,N)
    cov_f=np.cov(factor.T).reshape(L,L)
    GRS = (T * 1.0 / N) * ((T - N - L) * 1.0 / (T - L - 1)) \
          * (alpha.T * np.linalg.inv(cov_e) * alpha)\
          / (1 + mu_mean.T * np.linalg.inv(cov_f) * mu_mean)
    pvalue = scipy.stats.f.sf(GRS, N, (T - N - L))
    return GRS[0,0],pvalue[0,0]


def summary_statistics(data,percentiles=[0.05, 0.25, 0.5, 0.75, 0.95],axis=1):
    '''
    calculate the summary statistics.
    Args:
        data: pandas Series or pandas DataFrame.
        axis: 0 or 1
            If 0,take out a column each time and summary this column along the index.
            That is,summarize column by column.
    Returns:series or dataframe.

    References:
        pandas.DataFrame.describe()
    '''
    def describe_1d(series,percentiles):
        stat_index=(['mean','std','skew','kurt','min']+
                    format_percentiles(percentiles)+['max','n'])
        d=([series.mean(),series.std(),series.skew(),series.kurt(),series.min()]+
            [series.quantile(x) for x in percentiles]+[series.max(),series.count()])
        return pd.Series(d,index=stat_index,name=series.name)

    if data.ndim==1:
        return describe_1d(data,percentiles)
    else:
        if axis==0:
            ldesc=[describe_1d(s,percentiles) for _,s in data.iteritems()]
        elif axis==1:
            ldesc = [describe_1d(s,percentiles) for _, s in data.T.iteritems()]
        summary=pd.concat(ldesc,axis=1)
    return summary.T

def corr(df,method='pearson',winsorize=False):
    '''
    compare with the method in dataframe,this function will automatically winsorize the values
    before calculating Pearson correlations.

    Args:
        data:
        method: {'pearson','spearman'},'pearson' denotes Pearson product-moment correlation
            'spearman' denotes the Spearman rank correlation.Values are winsorized prior to
            calculate the Pearson product-moment correlation.When calculating the Spearman
            rank correlation,the data should not be winsorized.

    Returns:

    '''
    if winsorize==True:
        df = pandasu.winsorize(df, (0.01, 0.01), axis = 0)

    if method=='pearson':
        return df.corr(method='pearson')
    elif method=='spearman':
        return df.corr(method='spearman')

#persistance
def persistence(df,offsets):
    '''
    calculate cross-sectional Pearson product-moment correlations
    between indicator mesured in time t with indicator measured in
    t+offset.

    Returns:

    References:
        chapter 4.1.1 of (Bali, Turan G., Robert F. Engle, and Scott Murray. Empirical Asset Pricing:
        The Cross Section of Stock Returns. Hoboken, New Jersey: Wiley, 2016.)

    '''
    def _cross_persistence(df,offset):
        inds=df.index.tolist()
        series = pd.Series(name=offset)
        for i in range(len(inds[:-offset])):
            corrdf=df.iloc[[i,i+offset],:].T
            corr=corrdf.corr()
            series[inds[i]]=corr.iloc[0,1]
        return series

    lcorr = [_cross_persistence(df,offset) for offset in offsets]
    persistence = pd.concat(lcorr, axis=1)
    avg = persistence.mean()
    return avg


def cal_breakPoints(df,q):
    '''
    If the q is an integer,the function will return the breakpoints
    to break the data into q portfolios,that is it will create q+1
    breakpoints.If the q is a list of quantiles,then the function will
    create breakpoints according the given quantiles.

    Args:
        df: dataframe
        q: integer or array of quantiles

    Returns:

    '''

    if isinstance(q,int):
        points=np.linspace(0,1.0,q+1)
    else:
        points=q
    def _get_quantiles(series,points,name):
        d=[series.quantile(bp) for bp in points]
        return pd.Series(d,index=format_percentiles(points),name=name)
    lbps=[_get_quantiles(s,points,name) for name,s in df.iterrows()]
    breakPoints=pd.concat(lbps,axis=1)
    return breakPoints.T

def count_groups(df,q):
    '''
    Count the number of stocks for each group,given the quantiles or
    the number of groups

    Args:
        df:
        q: integer or array of quantiles
            Number of quantiles. 10 for deciles, 4 for quartiles, etc. Alternately
            array of quantiles, e.g. [0, .25, .5, .75, 1.] for quartiles
    Returns:

    '''
    if isinstance(q,int):
        lbs=['g'+str(i) for i in range(1,q+1)]
        ln=[pd.qcut(df.loc[month],q,labels=lbs).value_counts()
            for month in df.index.tolist()]
    else:
        lbs=['g'+str(i) for i in range(1,len(q))]
        ln=[pd.qcut(df.loc[month],q,labels=lbs).values_counts()
            for month in df.index.tolist()]

    count=pd.concat(ln,axis=1)
    count = count.reindex_axis(lbs, axis=0)
    return count.T


def famaMacBeth(formula, time_label, df, lags=5):
    '''
    Fama-MacBeth regression with Newey-West correction.

        The only input required for the Newey and West (1987) adjustment is
    the number of lags to use when performing the adjustment. As discussed
    in Newey and West (1994), the choice of lags is arbitrary.Frequently,
    econometrics software sets the number of lags to 4(T/100)a, where T is
    the number of periods in the time series, a = 2/9 when using the Bartlett
    kernel, and a = 4/25 when using the quadratic spectral kernel to calculate
    the autocorrelation and heteroscedasticity-adjusted standard errors.A
    large proportion of empirical asset pricing studies use monthly samples
    covering the period from 1963 through the present (2012, or T = 600
    months for the data used in this book). Plugging in the value T = 600
    and taking a to be either 2/9 or 4/25 results in a value between five
    and six. Most studies, therefore, choose six as the number of lags.

    Args:
        formula:string like 'y ~ x'
        time_label:string
            choosen from the df.columns,it used to indicate which column is time
        df:
        lags:int
            number of lags to use when performing the adjustment.
            If lags==0,it will forgo the Newey-West correction.

    Returns:DataFrame

    References:
        1.http://www.kellogg.northwestern.edu/faculty/petersen/htm/papers/se/se_programming.htm

        2.Fama, Eugene F., and James D. MacBeth. “Risk, Return, and Equilibrium:
        Empirical Tests.” Journal of Political Economy 81, no. 3 (May 1, 1973):
         607–36. https://doi.org/10.1086/260061.

        3.Bali, Turan G., Robert F. Engle, and Scott Murray. Empirical Asset
        Pricing: The Cross Section of Stock Returns. Hoboken, New Jersey: Wiley, 2016.

    Examples:
        from urllib import urlopen
        filehandle = urlopen('http://www.kellogg.northwestern.edu/faculty/petersen/htm/papers/se/test_data.txt')
        df = pd.read_table(filehandle, names=['firmid','year','x','y'],
                  delim_whitespace=True)

        famaMacBeth('y ~ x','year',df,lags=3)

                   coef    stderr     tvalue        pvalue stars
        Intercept  0.031278  0.021295   1.468810  1.759490e-01
        x          1.035586  0.025883  40.010988  1.893637e-11   ***

    '''
    res = df.groupby(time_label).apply(lambda x: sm.ols(
        formula, data=x).fit())
    l = [x.params for x in res]
    p = pd.DataFrame(l)

    means = {}
    params_labels = res.iloc[0].params.index

    # The ':' character used by patsy doesn't play well with pandas
    # column names.
    p.columns = [x.replace(':', '_INTER_') for x in p.columns]

    for x in p.columns:
        if lags is 0:
            means[x.replace('_INTER_', ':')] = sm.ols(formula=x + ' ~ 1',
                                                      data=p[[x]]).fit(use_t=True)
        else:
            means[x.replace('_INTER_', ':')] = sm.ols(formula=x + ' ~ 1',
                                                      data=p[[x]]).fit(cov_type='HAC',
                                                                       cov_kwds={'maxlags': lags},
                                                                       use_t=True)
    params = []
    stderrs = []
    tvalues = []
    pvalues = []
    for x in params_labels:
        params.append(means[x].params['Intercept'])
        stderrs.append(means[x].bse['Intercept']) #trick: stderr = std / sqrt(n-1)
        tvalues.append(means[x].tvalues['Intercept'])
        pvalues.append(means[x].pvalues['Intercept'])

    result = pd.DataFrame([params, stderrs, tvalues, pvalues]).T
    result.index = params_labels
    result.columns = ['coef', 'stderr', 'tvalue', 'pvalue']
    result['stars'] = ''
    result.loc[result.pvalue < 0.1, 'stars'] = '*'
    result.loc[result.pvalue < 0.05, 'stars'] = '**'
    result.loc[result.pvalue < 0.01, 'stars'] = '***'

    return result

