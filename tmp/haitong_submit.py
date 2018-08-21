# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-08-19  10:41
# NAME:zht-HaiTong_hp_new.py

import multiprocessing
import pickle

import pandas as pd
import os
import numpy as np
import scipy
import statsmodels.api as sm
from cvxopt import solvers,matrix
import matplotlib.pyplot as plt
from cvxpy import Variable, Minimize, Maximize, Problem, norm
import cvxpy

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
    r = F.T @ r_f, predicted stock return

E : K x K, 
    covariance matrix of factor return (realized), risk matrix of factors,
    and this can also be used as the predicted covariance matrix of factors

l_p: K x 1, exposure on factor for portfolio
    l_p = F @ w

l_b: K x 1, exposure on factor for benchmark
    l_b = F @ w_b

r_p: N x 1, predicted portfolio return 
    r_p = w.T @ r_s = w.T @ (F.T @ r_f)

risk_p: 1 x 1, portfolio risk = factor risk + specific risk
    risk_p = (l_p.T @ E @ l_p) + (w.T @ M @ w)
           = (w.T @ F.T @ E @ F @ w) + (w.T @ M @ w)
           = (w.T @ (F.T @ E @ F) @ w) + (w.T @ M @ w)

rc : K x 1, risk contribution
    np.multiply(F @ (w-w_b),E @ F @ (w-w_b))/((w-w_b).T @ (F.T @ E @ F ) @ (w-w_b))
    np.multiply denotes hadamard product

risk_active: 1 x 1, active risk, 
    G_active = (w - w_b).T @ ( F.T @ E @ F) @ (w - w_b) 

# S : N x N,
#     triangular Choelsky factor of E such that C.T @ C = E

'''


DIR=r'E:\tmp_haitong\haitong_new'
DIR_RAW=os.path.join(DIR,'raw_data')
DIR_TMP=os.path.join(DIR,'tmp_data')
DIR_RESULT=os.path.join(DIR,'result')

FACTORS=['log_size','bp','cumRet','turnover','amihud','ivol']
WINDOW_HISTORY=12 # window to calculate the predicted factor return



def get_indicators():
    fdmt=read_local('equity_fundamental_info')
    trading = read_local('equity_selected_trading_data')

    # size
    size=pd.pivot_table(fdmt,'cap','trd_dt','stkcd')
    size=size.resample('M').last()
    size.to_pickle(os.path.join(DIR,'size.pkl'))

    # log_size
    log_size=np.log(size)
    log_size.to_pickle(os.path.join(DIR,'log_size.pkl'))

    #bp
    bp=pd.read_pickle(r'G:\FT_Users\HTZhang\FT\singleFactor\indicators\V__bp.pkl')
    bp=bp.resample('M').last()
    bp.to_pickle(os.path.join(DIR,'bp.pkl'))

    # cumRet
    adjclose = pd.pivot_table(trading, values='adjclose', index='trd_dt',
                              columns='stkcd')
    adjcloseM=adjclose.resample('M').last()
    cumRet=adjcloseM.pct_change()
    cumRet.to_pickle(os.path.join(DIR,'cumRet.pkl'))

    ret=cumRet.copy()
    ret.to_pickle(os.path.join(DIR,'ret.pkl'))


    # turnover
    comb=pd.concat([trading,fdmt],axis=1)
    comb['turnover1']=comb['amount']/comb['freeshares']
    turnover=pd.pivot_table(comb,'turnover1','trd_dt','stkcd')
    turnover=turnover.resample('M').mean()
    turnover.to_pickle(os.path.join(DIR,'turnover.pkl'))

    # amihud
    amihud=pd.read_csv(os.path.join(DIR,'Liq_Amihud_M.csv'))
    amihud['EndD']=pd.to_datetime(amihud['EndD'])
    amihud['Stkcd']=amihud['Stkcd'].astype(str)
    def convert_stkcd(s):
        if len(s)==6:
            if s.startswith('3'):
                return s+'.SZ'
            else:
                return s+'.SH'
        else:
            return '0'*(6-len(s))+s+'.SZ'
    amihud['Stkcd']=amihud['Stkcd'].map(convert_stkcd)
    amihud=pd.pivot_table(amihud,'ILLIQ_M','EndD','Stkcd')
    amihud=amihud.resample('M').last()
    amihud.to_pickle(os.path.join(DIR,'amihud.pkl'))

    # idiosyncratic volatility

    # ivol=pd.read_pickle(r'G:\FT_Users\HTZhang\FT\singleFactor\indicators\T__idioVol_180.pkl')
    # ivol=ivol.resample('M').last()
    # ivol.to_pickle(os.path.join(DIR,'ivol.pkl'))
    idio=pd.read_pickle(r'G:\FT_Users\HTZhang\haitong\raw\idio.pkl')
    ivol=pd.pivot_table(idio,'vol_6M__D','t','sid')
    cols=[convert_stkcd(c) for c in ivol.columns]
    ivol.columns=cols
    ivol.to_pickle(os.path.join(DIR,'ivol.pkl'))


def multi_task(func, args_iter, n=8):
    pool=multiprocessing.Pool(n)
    results=pool.map(func, args_iter)
    pool.close()
    pool.join()
    return results


def outlier(s, k=4.5):
    '''
    Parameters
    ==========
    s:Series
        原始因子值
    k = 3 * (1 / stats.norm.isf(0.75))
    '''
    med = np.median(s)
    mad = np.median(np.abs(s - med))
    uplimit = med + k * mad
    lwlimit = med - k * mad
    y = np.where(s >= uplimit, uplimit, np.where(s <= lwlimit, lwlimit, s))
    # return pd.DataFrame(y, index=s.index)
    return pd.Series(y, index=s.index)

def z_score(x):
    return (x - np.mean(x)) / np.std(x)


def clean_raw_factors():
    for factor in FACTORS:
        s=pd.read_pickle(os.path.join(DIR_RAW,factor+'.pkl')).stack().swaplevel()
        s.name=factor
        fdmt=pd.read_pickle(os.path.join(DIR_RAW,'fdmt_m.pkl'))
        data = pd.concat([fdmt, s], axis=1, join='inner')
        data.index.names=['stkcd','month_end']

        data = data.dropna(subset=['type_st', 'young_1year'])
        data = data[(~data['type_st']) & (~ data['young_1year'])]  # 剔除st 和上市不满一年的数据
        data=data.dropna(subset=[factor])
        data[factor+'_out']=data.groupby('month_end')[factor].apply(outlier)
        data[factor+'_zsc']=data.groupby('month_end')[factor+'_out'].apply(z_score)
        cleaned=pd.pivot_table(data,factor+'_zsc','month_end','stkcd')
        cleaned.to_pickle(os.path.join(DIR_TMP,factor+'.pkl'))
        print(factor)

def get_factor_loading():
    ss=[]
    for factor in FACTORS:
        if factor =='cumRet':
            s=pd.read_pickle(os.path.join(DIR_TMP,factor+'.pkl')).fillna(0).dropna(axis=0,how='all').stack()
        elif factor=='amihud':
            s=pd.read_pickle(os.path.join(DIR_TMP,factor+'.pkl')).ffill().dropna(axis=0,how='all').stack()*(-1)
        else:
            s=pd.read_pickle(os.path.join(DIR_TMP,factor+'.pkl')).ffill().dropna(axis=0,how='all').stack()

        ss.append(s)
    factor_loading=pd.concat(ss,axis=1,join='inner',keys=FACTORS)
    factor_loading.index.names = ['month_end', 'stkcd']
    factor_loading.to_pickle(os.path.join(DIR_TMP,'factor_loading.pkl'))

def reg(df):
    y=df['ret']
    X=df[['const']+FACTORS]
    r=sm.OLS(y,X).fit()
    return r

def get_realized_factor_return():
    factor_loading=pd.read_pickle(os.path.join(DIR_TMP,'factor_loading.pkl'))
    comb = factor_loading.groupby('stkcd').shift(1)
    ret = pd.read_pickle(os.path.join(DIR_RAW, 'ret.pkl')).stack()
    comb['ret'] = ret
    comb = comb.dropna()
    # comb.to_pickle(os.path.join(DIR, 'comb.pkl'))
    comb=sm.add_constant(comb)
    rs=comb.groupby('month_end').apply(reg)
    realized_factor_return=pd.concat([r.params[1:] for r in rs],axis=1,keys=rs.index).T
    realized_factor_return.to_pickle(os.path.join(DIR_TMP,'realized_factor_return.pkl'))

def get_predicted_factor_return():
    factor_return=pd.read_pickle(os.path.join(DIR_TMP,'realized_factor_return.pkl'))
    predicted=factor_return.rolling(WINDOW_HISTORY).mean().shift(1)
    predicted.to_pickle(os.path.join(DIR_TMP,'predicted_factor_return.pkl'))

# get_factor_loading()
# get_realized_factor_return()
# get_predicted_factor_return()

def get_zz500_weight():
    indexweight=pd.read_csv(os.path.join(DIR_RAW,'aindexhs300freeweight.csv'),names=['id','s_info_windcode','s_con_windcode','trade_dt','i_weight','opdate','opmode'])
    indexweight['s_info_windcode'].value_counts()
    weight_zz500=indexweight[indexweight['s_info_windcode']=='000905.SH']
    weight_zz500['trade_dt']=pd.to_datetime(weight_zz500['trade_dt'].astype(str))
    con_weight=pd.pivot_table(weight_zz500,'i_weight','trade_dt','s_con_windcode')
    con_weight=con_weight.resample('M').last()/100
    con_weight.to_pickle(os.path.join(DIR_TMP,'zz500_weight.pkl'))

def optimize0(N, F, r_f):
    #==========================maximize portfolio return=============================
    w = Variable((N, 1))
    r_p = w.T @ (F.T @ r_f)
    obj = Maximize(r_p)
    constraints0=[
                sum(w)==1.0,
                0.0<=w,
                w<=0.01]
    prob0=Problem(obj,constraints0)
    # prob0.solve(solver=cvxpy.CVXOPT)
    prob0.solve(solver=cvxpy.ECOS)

    if abs(sum(w.value)-1.0)>=0.01:
        raise ValueError('w0 sum >1.01')
    if min(w.value)<-0.001:
        raise ValueError('w1 min < -0.001')

    return w.value

def optimize1(N,F,r_f,E,w_b,tracking_error=0.05):
    #=================maximize portfolio return with constraints on active risk=======================
    w=Variable((N,1))
    r_p = w.T @ (F.T @ r_f)
    risk=cvxpy.quad_form(F @ (w - w_b),E)
    obj = Maximize(r_p)
    constraints=[
        sum(w)==1,
        0.0<=w,
        w<=0.01,
        risk<=tracking_error*tracking_error/12
    ]
    prob=Problem(obj,constraints)
    prob.solve(cvxpy.ECOS)

    #check the solution
    if abs(sum(w.value) - 1.0) >= 0.01:
        raise ValueError('w0 sum >1.01')
    if min(w.value) < -0.001:
        raise ValueError('w1 min < -0.001')

    return w.value

def optimize2(N,F,r_f,w_b,style_deviation=1.0):
    w=Variable((N,1))
    r_p = w.T @ (F.T @ r_f)
    sd=F @ (w - w_b)
    obj = Maximize(r_p)
    constraints=[
        sum(w)==1,
        0.0<=w,
        w<=0.01,
        -style_deviation<=sd,
        sd<=style_deviation
    ]
    prob=Problem(obj,constraints)
    prob.solve(cvxpy.ECOS)

    #check the solution
    if abs(sum(w.value) - 1.0) >= 0.01:
        raise ValueError('w0 sum >1.01')
    if min(w.value) < -0.001:
        raise ValueError('w1 min < -0.001')

    return w.value

def optimize3(N,F,r_f,w_b,size_matrix,style_deviation=0.5):
    '''

    :param N:
    :param F:
    :param r_f:
    :param w_b:
    :param size_matrix:M x N,
        M denotes the number of portfolios constructed by soring on size
    :return:
    '''
    w=Variable((N,1))
    r_p = w.T @ (F.T @ r_f)

    obj = Maximize(r_p)

    sd=F @ (w - w_b)

    constraints=[
        sum(w)==1,
        0.0<=w,
        w<=0.01,
        size_matrix @ (w - w_b)==0,
        -style_deviation<=sd,
        sd<=style_deviation
    ]
    prob=Problem(obj,constraints)
    prob.solve()
    print(prob.status)

    #check the solution
    # if abs(sum(w.value) - 1.0) >= 0.01:
    #     raise ValueError('w0 sum >1.01')
    # if min(w.value) < -0.001:
    #     raise ValueError('w1 min < -0.001')

    return w.value

def get_size_matrix(cap,number=10):
    gs=pd.qcut(cap,number,labels=range(1,number+1))
    dummy_matrix=np.matrix(pd.get_dummies(gs)).T
    return dummy_matrix

def solve_one_month(args):
    t, factor_loading_groups, zz500_weight, factor_risk_cov, predicted_factor_return,fdmt,mode=args
    _fl = factor_loading_groups.get_group(t)
    _fl.index = _fl.index.droplevel(level=0)
    _zw = zz500_weight.loc[t]
    cap=fdmt.loc[(slice(None),t),'cap']
    cap.index=cap.index.droplevel(level=1)

    stkcd_inter=_fl.index.intersection(cap.index)
    _fl=_fl.reindex(stkcd_inter)
    cap=cap.reindex(stkcd_inter)
    _zw = _zw.reindex(_fl.index).fillna(0)

    size_matrix = get_size_matrix(cap)
    cov = factor_risk_cov.loc[(t, slice(None)), :]
    F = np.matrix(_fl.T)
    r_f = np.matrix(predicted_factor_return.loc[t]).T
    # K = F.shape[0]
    N = F.shape[1]
    w_b = np.matrix(_zw).T
    E = np.matrix(cov)

    # mode_map={
    #     0:optimize0(N,F,r_f),
    #     1:optimize1(N,F,r_f,E,w_b,0.05),
    #     2:optimize1(N,F,r_f,E,w_b,0.03),
    #     3:optimize2(N,F,r_f,w_b,1),
    #     4:optimize2(N,F,r_f,w_b,0.5),
    #     5:optimize3(N,F,r_f,w_b,size_matrix,0.5),
    # }

    if mode==0:
        w=optimize0(N,F,r_f)
    elif mode==1:
        w=optimize1(N,F,r_f,E,w_b,0.05)
    elif mode==2:
        w=optimize1(N,F,r_f,E,w_b,0.03)
    elif mode==3:
        w=optimize2(N, F, r_f, w_b, 1)
    elif mode==4:
        w=optimize2(N, F, r_f, w_b, 0.5)
    elif mode==5:
        w=optimize3(N, F, r_f, w_b, size_matrix, 0.5)

    # exposure on factor
    l_b=pd.Series(np.array(F @ w_b).reshape(-1,),index=_fl.columns)
    l_b.name=t

    l_p=pd.Series(np.array(F @ w).reshape(-1,),index=_fl.columns)
    l_p.name=t

    # risk contribution relative to benchmark
    rc=np.multiply(F @ (w-w_b),E @ F @ (w-w_b))/((w-w_b).T @ (F.T @ E @ F ) @ (w-w_b))
    rc=pd.Series(np.array(rc).reshape(-1,),index=_fl.columns)
    rc.name=t

    # solution
    w=pd.Series(w.reshape(-1),index=_fl.index)
    w.name=t

    result={}
    for nm in ['w','l_b','l_p','rc']:
        result[nm]=eval(nm)
    print(t)
    return result

def stats_performance(comb):
    comb=comb['2011-02':'2017-05']
    risk_free=0.0
    portfolio_value=(comb['hedged']+1).cumprod()
    hedged_return=portfolio_value[-1]**(252/len(comb))-1 # annualized return
    tracking_error=comb['hedged'].std()*pow(255,0.5) # annualized tracking error
    max_drawdown = 1 - min(portfolio_value / np.maximum.accumulate(
        portfolio_value.fillna(-np.inf)))
    information_ratio=(hedged_return-risk_free)/tracking_error
    return_down_ratio=hedged_return/max_drawdown

    indicators=['hedged_return','tracking_error','max_drawdown','information_ratio','return_down_ratio']
    perf=pd.Series([hedged_return,tracking_error,max_drawdown,information_ratio,return_down_ratio],index=indicators)
    return perf

def get_results(mode):
    fdmt = pd.read_pickle(os.path.join(DIR_RAW, 'fdmt_m.pkl'))
    realized_factor_return=pd.read_pickle(os.path.join(DIR_TMP,'realized_factor_return.pkl'))
    factor_risk_cov=realized_factor_return.rolling(60).cov()
    factor_loading=pd.read_pickle(os.path.join(DIR_TMP,'factor_loading.pkl'))
    predicted_factor_return=pd.read_pickle(os.path.join(DIR_TMP,'predicted_factor_return.pkl'))

    zz500_weight=pd.read_pickle(os.path.join(DIR_TMP,'zz500_weight.pkl'))
    factor_loading_groups=factor_loading.groupby('month_end')
    ts=predicted_factor_return['2011':'2017-05'].index

    args_generator=((t, factor_loading_groups, zz500_weight, factor_risk_cov, predicted_factor_return,fdmt,mode) for t in ts)
    # results=multi_task(solve_one_month,args_generator,3)
    results=[solve_one_month(args) for args in args_generator] #TODO: use multi_task
    f=open(os.path.join(DIR_TMP,'results_{}.pkl'.format(mode)),'wb')
    pickle.dump(results,f)

def get_performance(mode):
    # get_results()
    results=pickle.load(open(os.path.join(DIR_TMP,'results_{}.pkl'.format(mode)),'rb'))
    weight=pd.concat([r['w'] for r in results],axis=1,sort=True).T.sort_index()# review:

    trading = pd.read_pickle(os.path.join(DIR_RAW, 'equity_selected_trading_data.pkl'))
    retD = pd.pivot_table(trading, 'pctchange', 'trd_dt', 'stkcd') / 100.0
    retD=retD['2011':'2017-05']

    weight = weight.shift(1, freq='D').resample('D').pad()
    weight=weight.reindex(index=retD.index,columns=retD.columns)
    portfolio_retD = (weight * retD).sum(axis=1).dropna(how='all')

    zz500 = pd.read_pickle(os.path.join(DIR_RAW, 'zz500.pkl'))
    comb = pd.concat([portfolio_retD, zz500], axis=1, keys=['portfolio', 'zz500'])
    comb['hedged'] = comb['portfolio'] - comb['zz500']
    hedged=comb['hedged']['2011':'2017-05'].copy()
    hedged.to_pickle(os.path.join(DIR_RESULT,'pnl_{}.pkl'.format(mode)))

    performance=stats_performance(comb)
    performance.to_pickle(os.path.join(DIR_RESULT,'performance_{}.pkl'.format(mode)))

    # plot pnl
    comb = comb['2011':]
    (1 + comb['hedged']).cumprod().plot()
    plt.savefig(os.path.join(DIR_RESULT,'backtest_{}.png'.format(mode)))
    plt.close()

def get_style_exposure_fig(mode):
    results=pickle.load(open(os.path.join(DIR_TMP,'results_{}.pkl'.format(mode)),'rb'))

    lp=pd.concat([r['l_p'] for r in results],axis=1,sort=False).T
    lp.mean().plot.barh(rot=1)
    lp.mean().to_pickle(os.path.join(DIR_RESULT,'style_exposure_{}.pkl'.format(mode)))
    plt.savefig(os.path.join(DIR_RESULT,'style_exposure_{}.png'.format(mode)))
    plt.close()

def get_style_deviation(mode):
    results=pickle.load(open(os.path.join(DIR_TMP,'results_{}.pkl'.format(mode)),'rb'))
    lp=pd.concat([r['l_p'] for r in results],axis=1,sort=False).T
    lb=pd.concat([r['l_b'] for r in results],axis=1,sort=False).T
    (lp.mean()-lb.mean()).plot.barh(rot=1)
    (lp.mean()-lb.mean()).to_pickle(os.path.join(DIR_RESULT,'style_deviation_{}.pkl'.format(mode)))
    plt.savefig(os.path.join(DIR_RESULT,'style_deviation_{}.png'.format(mode)))
    plt.close()

def get_risk_constribution(mode):
    results=pickle.load(open(os.path.join(DIR_TMP,'results_{}.pkl'.format(mode)),'rb'))
    rc=pd.concat([r['rc'] for r in results],axis=1,sort=False).T
    rc.mean().plot.pie()
    plt.savefig(os.path.join(DIR_RESULT,'rc_{}.png'.format(mode)))
    plt.close()
    rc.mean().to_pickle(os.path.join(DIR_RESULT,'rc_{}.pkl'.format(mode)))

def run(mode):
    # get_results(mode)
    get_performance(mode)
    get_style_exposure_fig(mode)
    get_style_deviation(mode)
    get_risk_constribution(mode)

def summarize():
    modes=range(6)
    titles=[u'最大化预期收益',u'约束组合跟踪误差0.05',u'约束组合跟踪误差0.03',u'控制风格偏离1',u'控制风格偏离0.5',u'匹配风险因子分布']

    #==========================pnl============================
    pnl=pd.concat([pd.read_pickle(os.path.join(DIR_RESULT,'pnl_{}.pkl'.format(mode))) for mode in modes],axis=1,keys=titles)
    plt.rcParams['font.sans-serif']=['SimHei']
    # (1+pnl).cumprod().plot().get_figure().savefig(os.path.join(DIR_RESULT,'pnl.png'))

    fig,axes=plt.subplots(1,6,figsize=(30,3))
    for i in range(6):
        axes[i].plot(pnl.index,(1+pnl[pnl.columns[i]]).cumprod(),label=pnl.columns[i])
        axes[i].legend(loc='best')

    plt.savefig(os.path.join(DIR_RESULT,'pnl.png'))
    plt.close()

    #==============================performance======================
    performance=pd.concat([pd.read_pickle(os.path.join(DIR_RESULT,'performance_{}.pkl'.format(mode))) for mode in modes],axis=1,keys=titles)
    performance.to_csv(os.path.join(DIR_RESULT,'performance.csv'),encoding='gbk')

    rc=pd.concat([pd.read_pickle(os.path.join(DIR_RESULT,'rc_{}.pkl'.format(mode))) for mode in modes],axis=1,keys=titles)
    rc.to_csv(os.path.join(DIR_RESULT,'risk_contribution.csv'),encoding='gbk')

    plt.style.use('ggplot')
    colors = plt.rcParams['axes.color_cycle']
    plt.rcParams['font.sans-serif']=['SimHei']

    fig, axes = plt.subplots(1, 6, figsize=(20, 5))
    for ax, col in zip(axes, rc.columns):
        ax.pie(rc[col], labels=rc.index, autopct='%.2f', colors=colors)
        ax.set(ylabel='', title=col, aspect='equal')

    axes[0].legend(bbox_to_anchor=(0, 0.5))
    plt.savefig(os.path.join(DIR_RESULT, 'rc.png'))
    plt.close()

    #============================sd===================================
    sd=pd.concat([pd.read_pickle(os.path.join(DIR_RESULT,'style_deviation_{}.pkl'.format(mode))) for mode in modes],axis=1,keys=titles)
    sd.to_csv(os.path.join(DIR_RESULT,'style_deviation.csv'),encoding='gbk')

    plt.rcParams['font.sans-serif']=['SimHei']
    sd.plot(kind='bar',rot=1)
    plt.title('相对zz500的风格偏离')
    plt.savefig(os.path.join(DIR_RESULT,'sd.png'))

    #======================sp============================
    sp=pd.concat([pd.read_pickle(os.path.join(DIR_RESULT,'style_exposure_{}.pkl'.format(mode))) for mode in modes],axis=1,keys=titles)
    sp.to_csv(os.path.join(DIR_RESULT,'style_exposure.csv'),encoding='gbk')



if __name__ == '__main__':
    for mode in range(6):
        run(mode)
    summarize()

