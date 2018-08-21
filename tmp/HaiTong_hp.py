# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-08-17  00:29
# NAME:FT_hp-HaiTong.py
import multiprocessing

import pandas as pd
import os
import numpy as np
import statsmodels.api as sm
from cvxopt import solvers,matrix
import matplotlib.pyplot as plt
from cvxpy import Variable

DIR=r'E:\tmp_haitong'
DIR_RESULT=os.path.join(DIR,'result')

'''
N : number of stocks 
K : number of factors, CAPITAL denotes Matrix and lowercase denotes array (one column matrix)
=========
F : K x N, 
    factor loading (indicators)
    
M : N x N, 
    covariance matrix of stock returns, specific risk
    
w : N x 1, 
    target weight on stocks
    
w_b: N x 1,benchmark weight on stocks

r_f : K x 1,
    predicted factor return, usually use the history mean value of factor return

r_s : N x 1, 
    r = F.T @ f, predicted stock return

E : K x K, 
    covariance matrix of factor return (realized), risk matrix of factors,
    and this can also be used as the predicted covariance matrix of factors

l_p: K x 1, factor loading of portfolio
    l_p = F @ w

l_b: K x 1, factor loading of benchmark
    l_b = F @ w_b

r_p: N x 1, predicted portfolio return 
    r_p = u.T @ w

risk_p: 1 x 1, portfolio risk = factor risk + specific risk
    risk_p = (l_p.T @ E @ l_p) + (w.T @ M @ w)
           = (w.T @ F.T @ E @ F @ w) + (w.T @ M @ w)
           = (w.T @ (F.T @ E @ F) @ w) + (w.T @ M @ w)

rc : K x 1, risk contribution
    rc = (F @ w) * (E @ (F @ w)) /(w.T @ (F.T @ E @ F) @ w)

risk_active: 1 x 1, active risk, 
    G_active = (w - w_b).T @ ( F @ E @ F.T) @ (w - w_b) 

# S : N x N,
#     triangular Choelsky factor of E such that C.T @ C = E

'''



def outlier(s, k=4.5):
    '''
    Parameters
    ==========
    s:Series
        原始因子值
    k = 3 * (1 / stats.norm.isf(0.75))
    '''
    med = np.median(s) #debug: NaN should be removed before apply this function
    mad = np.median(np.abs(s - med))
    uplimit = med + k * mad
    lwlimit = med - k * mad
    y = np.where(s >= uplimit, uplimit, np.where(s <= lwlimit, lwlimit, s))
    # return pd.DataFrame(y, index=s.index)
    return pd.Series(y, index=s.index)

def z_score(x):
    return (x - np.mean(x)) / np.std(x)


indNames=['size','log_size','bp','cumRet','turnover','amihud','ivol']

def clean_indicators():
    for indname in indNames:
        s=pd.read_pickle(os.path.join(DIR,indname+'.pkl')).stack().swaplevel()
        s.name=indname

        fdmt_m = read_local('fdmt_m')
        data = pd.concat([fdmt_m, s], axis=1, join='inner')
        data.index.names=['stkcd','month_end']

        data = data.dropna(subset=['type_st', 'young_1year'])
        data = data[(~data['type_st']) & (~ data['young_1year'])]  # 剔除st 和上市不满一年的数据
        data=data.dropna(subset=[indname])
        data[indname+'_out']=data.groupby('month_end')[indname].apply(outlier)
        data[indname+'_zsc']=data.groupby('month_end')[indname+'_out'].apply(z_score)
        cleaned=pd.pivot_table(data,indname+'_zsc','month_end','stkcd')
        cleaned.to_pickle(os.path.join(DIR,'standardized',indname+'.pkl'))
        print(indname)


def get_factor_loading():
    dfs = []
    for indname in indNames:
        _df = pd.read_pickle(
            os.path.join(DIR, 'standardized', indname + '.pkl'))
        if indname is not 'cumRet':
            _df = _df.ffill()
        _df = _df.dropna(axis=0, how='all').stack()
        dfs.append(_df)

    factor_loading = pd.concat(dfs, axis=1, keys=indNames, join='inner')
    factor_loading.index.names = ['month_end', 'stkcd']
    factor_loading.to_pickle(os.path.join(DIR,'factor_loading.pkl'))

def reg(df):
    y=df['ret']
    X=df[['const']+indNames]
    r=sm.OLS(y,X).fit()
    return r

def get_factor_return():
    factor_loading=pd.read_pickle(os.path.join(DIR,'factor_loading.pkl'))
    comb = factor_loading.groupby('stkcd')
    ret = pd.read_pickle(os.path.join(DIR, 'cumRet.pkl')).stack()
    comb['ret'] = ret
    comb = comb.dropna()
    comb.to_pickle(os.path.join(DIR, 'comb.pkl'))
    comb=sm.add_constant(comb)
    rs=comb.groupby('month_end').apply(reg)
    factor_return=pd.concat([r.params[1:] for r in rs],axis=1,keys=rs.index).T
    factor_return.to_pickle(os.path.join(DIR,'factor_return.pkl'))

def get_predicted_factor_return(history_window=12):
    factor_return=pd.read_pickle(os.path.join(DIR,'factor_return.pkl'))
    predicted=factor_return.rolling(history_window).mean().shift(1)# trick:use the indicator of time t-1 to regress on return of time t
    predicted.to_pickle(os.path.join(DIR,'predicted_factor_return.pkl'))

get_factor_return()
get_predicted_factor_return()


def max_return(mu):
    P = matrix(np.zeros((len(mu), len(mu))))
    q = -matrix(mu)
    G = matrix(np.vstack((np.eye(len(mu)), -np.eye(len(mu)))))
    h = matrix([0.01] * len(mu) + [0.0] * len(mu))
    A = matrix([1.0] * len(mu)).T
    b = matrix(1.0)
    sol = solvers.qp(P, q, G, h, A, b)
    return sol['x']

def multi_task(func, args_iter, n=4):
    pool=multiprocessing.Pool(n)
    results=pool.map(func, args_iter)
    pool.close()#trick: close the processing every time the pool has finished its task, and pool.close() must be called before pool.join()
    pool.join()
    #refer to https://stackoverflow.com/questions/38271547/when-should-we-call-multiprocessing-pool-join
    return results

def task(args):
    factor_return_predicted,t,df=args
    fr = factor_return_predicted.loc[t]  # predicted factor return for t+1
    mu = np.matrix(df) @ np.matrix(fr).T
    weight = pd.Series(max_return(mu), index=df.index)
    return weight

def get_weight():
    factor_loading=pd.read_pickle(os.path.join(DIR,'factor_loading.pkl'))
    factor_return=pd.read_pickle(os.path.join(DIR,'factor_return.pkl'))

    WINDOW=12
    factor_return_predicted=factor_return.rolling(WINDOW).mean() #TODO: 12
    groups=factor_loading.groupby('month_end').groups
    args_generator=((factor_return_predicted,t,factor_loading.groupby('month_end').get_group(t)) for t in list(groups.keys())[WINDOW:])
    ws=multi_task(task,args_generator)
    w=pd.concat(ws)
    w.to_pickle(os.path.join(DIR,'weight.pkl'))

def get_zz500_weight():
    indexweight=pd.read_csv(os.path.join(DIR,'aindexhs300freeweight.csv'),names=['id','s_info_windcode','s_con_windcode','trade_dt','i_weight','opdate','opmode'])
    indexweight['s_info_windcode'].value_counts()
    weight_zz500=indexweight[indexweight['s_info_windcode']=='000905.SH']
    weight_zz500['trade_dt']=pd.to_datetime(weight_zz500['trade_dt'].astype(str))
    con_weight=pd.pivot_table(weight_zz500,'i_weight','trade_dt','s_con_windcode')
    con_weight=con_weight.resample('M').last()/100
    con_weight.to_pickle(os.path.join(DIR,'zz500_weight.pkl'))



factor_loading=pd.read_pickle(os.path.join(DIR,'factor_loading.pkl'))
factor_return=pd.read_pickle(os.path.join(DIR,'factor_return.pkl'))
WINDOW = 12
factor_return_predicted = factor_return.rolling(WINDOW).mean()  # TODO: 12
zz500_weight=pd.read_pickle(os.path.join(DIR,'zz500_weight.pkl'))


ts = factor_loading['2011':].index
t=ts[10]

factor_loading_gs=factor_loading.groupby('month_end')

_factor_loading=factor_loading_gs.get_group(t)
_zz500_weight=zz500_weight.loc[t]

_factor_loading.index=_factor_loading.index.droplevel(level=0)
_zz500_weight=_zz500_weight.reindex(_factor_loading.index).fillna(0)





f=np.matrix(factor_return_predicted.loc[t]).T
F=np.matrix(_factor_loading)
w_b=np.matrix(_zz500_weight).T
C=F @ f


k=F.shape[0]
n=F.shape[1]

w=Variable(n,nonneg=True)
active_ret=(F @ f).T @ w
tracking_risk=



def get_zz500():
    # zz500_ret_d = read_local('equity_selected_indice_ir')['zz500_ret_d']
    # zz500_ret_d.to_pickle(r'G:\FT_Users\HTZhang\haitong\zz500.pkl')
    pass

def get_hedged_return():
    '''figure 1'''
    weight=pd.read_pickle(os.path.join(DIR,'weight.pkl')).unstack().shift(1)#trick: use the weight of time t
    weight=weight.fillna(0)

    trading=pd.read_pickle(os.path.join(DIR,'equity_selected_trading_data.pkl'))
    retD=pd.pivot_table(trading,'pctchange','trd_dt','stkcd')/100.0
    weightD=weight.shift(1,freq='D').resample('D').pad()
    retD=retD.reindex(index=weightD.index,columns=weightD.columns)
    portfolio_retD=(weightD*retD).sum(axis=1)

    zz500=pd.read_pickle(os.path.join(DIR,'zz500.pkl'))
    comb=pd.concat([portfolio_retD,zz500],axis=1,keys=['portfolio','zz500'])
    comb['hedged']=comb['portfolio']-comb['zz500']
    comb=comb['2011':]
    fig=(1+comb['hedged']).cumprod().plot().get_figure()
    fig.savefig(os.path.join(DIR_RESULT,'fig1'))


def _cal_risk_exposure(weight_df):
    factor_loading=pd.read_pickle(os.path.join(DIR,'factor_loading.pkl'))
    factor_loading=factor_loading.unstack()
    ts=factor_loading['2011':].index
    F_pt_s=[]
    for t in ts:
        _w=weight_df.loc[t].fillna(0)#trick: before calculate with matrix, fillna
        _fl=factor_loading.loc[t].unstack().reindex(index=indNames,columns=_w.index).fillna(0)
        F=np.array(_fl.T)# N x K
        w=_w.values.reshape((len(_w),1)) # N x 1
        F_pt=w.T @ F
        F_pt_s.append(F_pt.reshape(-1))
    F_pt=pd.DataFrame(F_pt_s,index=ts,columns=indNames)
    return F_pt



# port_weight=pd.read_pickle(os.path.join(DIR, 'weight.pkl')).unstack().shift(1)#trick: at time t+1，use weight calculated from time t
#
# weight_df=port_weight.copy()


def _cal_risk_exposure_old(weight_df):
    factor_loading=pd.read_pickle(os.path.join(DIR,'factor_loading.pkl'))
    ss=[]
    for col in factor_loading.columns:
        subdf=pd.pivot_table(factor_loading,col,'month_end','stkcd')
        exposure= subdf.reindex(index=weight_df.index, columns=weight_df.columns) * weight_df
        exposure=exposure.sum(axis=1)
        ss.append(exposure)
        print(col)
    exposure_df=pd.concat(ss,axis=1,keys=factor_loading.columns)
    return exposure_df
    # fig=exposure_df.mean().plot.bar(rot=1).get_figure()
    # return fig

def get_exposure_on_factor():
    port_weight=pd.read_pickle(os.path.join(DIR, 'weight.pkl')).unstack().shift(1)#trick: at time t+1，use weight calculated from time t
    # fig2=_cal_risk_exposure(port_weight)
    port_exposure=_cal_risk_exposure(port_weight)

    indexweight=pd.read_csv(os.path.join(DIR,'aindexhs300freeweight.csv'),names=['id','s_info_windcode','s_con_windcode','trade_dt','i_weight','opdate','opmode'])
    indexweight['s_info_windcode'].value_counts()
    weight_zz500=indexweight[indexweight['s_info_windcode']=='000905.SH']
    weight_zz500['trade_dt']=pd.to_datetime(weight_zz500['trade_dt'].astype(str))
    con_weight=pd.pivot_table(weight_zz500,'i_weight','trade_dt','s_con_windcode')
    con_weight=con_weight.resample('M').last().shift(1)/100#trick: use the weight of last month
    # fig3=_cal_risk_exposure(con_weight)
    zz500_exposure=_cal_risk_exposure(con_weight)

    port_exposure.to_pickle(os.path.join(DIR,'port_exposure.pkl'))
    zz500_exposure.to_pickle(os.path.join(DIR,'zz500_exposure.pkl'))


    port_exposure.mean().plot.bar(rot=1)
    plt.savefig(os.path.join(DIR_RESULT,'fig2.png'))
    plt.close()

    zz500_exposure.mean().plot.bar(rot=1)
    plt.savefig(os.path.join(DIR_RESULT,'fig3.png'))
    plt.close()


    # fig2.savefig(os.path.join(DIR_RESULT,'fig2.png'))
    # fig3.savefig(os.path.join(DIR_RESULT,'fig3.png'))


def get_fig4():
    port_exposure=pd.read_pickle(os.path.join(DIR,'port_exposure.pkl'))
    zz500_exposure=pd.read_pickle(os.path.join(DIR,'zz500_exposure.pkl'))

    factor_return=pd.read_pickle(os.path.join(DIR,'factor_return.pkl'))

    factor_risk_cov=factor_return.rolling(60).corr() #TODO: rolling window
    factor_risk_cov=factor_risk_cov.unstack().shift(1)#review: use the factor_risk of last period
    factor_risk_cov.to_pickle(os.path.join(DIR, 'factor_risk_cov.pkl'))


    ts=port_exposure['2011':].index #review: time window
    rc_s=[]
    _factor_risk_s=[]
    for t in ts:
        _port_exp=port_exposure.loc[t]
        _zz500_exp=zz500_exposure.loc[t]

        F=(_port_exp-_zz500_exp).values
        E=factor_risk_cov.loc[t].unstack()
        E=E.loc[_port_exp.index,_port_exp.index] #make sure that the data is one-to-one corresponce
        E=E.values

        rc=F * (E @ F)/(F.T @ E @ F)
        rc_s.append(rc)
        _factor_risk_s.append(F.T @ E @ F)
    RC=pd.DataFrame(rc_s,index=ts,columns=port_exposure.columns)
    factor_risk=pd.Series(_factor_risk_s, index=ts)
    factor_risk.to_pickle(os.path.join(DIR,'factor_risk.pkl'))

    fig4=RC.mean().plot.pie().get_figure()
    fig4.savefig(os.path.join(DIR_RESULT,'fig4.png'))




#TODO: change the direction of ivol


'''
the matrix is column-major order different with numpy

m1=cvxopt.matrix([[1,2,3],[4,5,6]])
m2=np.matrix([[1,2,3],[4,5,6]])

'''


# if __name__ == '__main__':
#     get_weight()



#zz500_ret_d = read_local('equity_selected_indice_ir')['zz500_ret_d']

