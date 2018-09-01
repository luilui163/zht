# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-01  22:27
# NAME:zht-base_on_foxit.py
import itertools
import multiprocessing
import os
import random

import numpy as np
from scipy import stats
from line_profiler import LineProfiler
import pandas as pd
from numba import jit

import statsmodels.api as sm


CRITIC=0.05

DIR=r'e:\tmp_kogan'

def multi_task(func, args_iter, n=4):
    pool=multiprocessing.Pool(n)
    results=pool.map(func, args_iter)
    pool.close()#trick: close the processing every time the pool has finished its task, and pool.close() must be called before pool.join()
    pool.join()
    #refer to https://stackoverflow.com/questions/38271547/when-should-we-call-multiprocessing-pool-join
    return results


def pricing_assets(benchmark, assets):
    '''
    use benchmark to pricing the assets and get the relevant parameters including
    betas,alpha stderr, resid
    Args:
        benchmark:
        assets: DataFrame, each column represent a realized asset

    Returns:

    '''
    # E:\FT_Users\HTZhang\software\python\HTZhang\FT_hp\empirical\kogan_part2.py
    X=sm.add_constant(benchmark)
    rs=[sm.OLS(assets[col],X).fit() for col in assets.columns]

    alpha=pd.Series([r.params['const'] for r in rs], index=assets.columns)
    alpha_stderr=pd.Series([r.bse['const'] for r in rs], index=assets.columns)
    alpha_t=pd.Series([r.tvalues['const'] for r in rs], index=assets.columns)
    alpha_p=pd.Series([r.pvalues['const'] for r in rs],index=assets.columns)
    betas=pd.concat([r.params[1:] for r in rs], axis=1, keys=assets.columns)
    resid=pd.DataFrame([r.resid for r in rs], index=assets.columns, columns=benchmark.index).T

    result={}
    for _name in ['alpha','alpha_stderr','alpha_t','alpha_p','betas','resid']:
        result[_name]=eval(_name)
    return result

def bootstrap_kogan(benchmark, assets, realized_result, anomaly_num):
    get_random_index = lambda: random.choices(benchmark.index,
                                              k=benchmark.shape[0])

    _01_list=[1]*anomaly_num+[0]*(len(realized_result['alpha'])-anomaly_num)
    random.shuffle(_01_list)
    is_anomaly=pd.Series(_01_list,index=realized_result['alpha'].index)
    assigned_alpha=realized_result['alpha_stderr'].map(lambda a:3*a*random.choice([-1,1]))*is_anomaly
    adjusted_assets=assets-realized_result['alpha']+assigned_alpha
    index=get_random_index()
    simulated_factors=adjusted_assets.loc[index]
    simulated_rp=benchmark['rp'].loc[index]
    simulated_factors=pd.concat([simulated_factors,simulated_rp],axis=1)
    return simulated_factors



@jit(nopython=True)
def get_matched_number_jit(X,Y):
    params = np.linalg.pinv(X.T @ X) @ X.T @ Y
    predictions = X @ params
    MSE=np.diag(np.transpose(Y-predictions) @ (Y-predictions))/(X.shape[0]-X.shape[1])
    A=np.diag(np.linalg.inv(np.transpose(X) @ X))
    # var_b=np.diag(np.matrix(A)) @ np.matrix(MSE)
    var_b=np.diag(A) @ MSE
    sd_b = np.sqrt(var_b)
    ts_b = params / sd_b
    # cal_pvalue = lambda t: 2 * (1 - stats.t.cdf(np.abs(t), X.shape[0] - 1))
    matched_num=0
    for x in np.nditer(ts_b[0]):
        v=2*(1-stats.t.cdf(np.abs(x),X.shape[0]-1)) #fixme: failed, numba does not support stats.t
        if v>CRITIC:
            matched_num+=1

    return matched_num

def get_matched_number(X,Y):
    '''
    use X to pricing Y, and count the number of asset that can be matched by X
    Args:
        X: array, X is benchmark.values, and the first column of X must be 'const'
        Y: array, Y is assets.values, the assets to be priced

    Returns:

    '''
    '''
    the firs column of model must be 'const'
    Args:
        model:
        assets:
        add_constant:

    Returns:

    '''
    params = np.linalg.pinv(X.T @ X) @ X.T @ Y
    predictions = X @ params

    #trick:split the the long equation can speed up signicantly, 10 time faster with this way
    # a=(Y-predictions).T
    # b=(Y-predictions)
    # c=a@b # use matrix rather than array ,or it will be 10 time slower
    # d=c.diagonal()
    # MSE=d/(X.shape[0]-X.shape[1])

    MSE = ((Y - predictions).T @ (Y - predictions)).diagonal() / (X.shape[0] - X.shape[1])
    A = np.linalg.inv(X.T @ X).diagonal()
    var_b=A.T @ MSE
    sd_b = np.sqrt(var_b)
    ts_b = params / sd_b
    cal_pvalue = lambda t: 2 * (1 - stats.t.cdf(np.abs(t), X.shape[0] - 1))

    # matched_num=0
    # for x in np.nditer(ts_b[0]):
    #     if cal_pvalue(x)>CRITIC:
    #         matched_num+=1
    #
    pvalues = np.vectorize(cal_pvalue)(ts_b[0])# only get the pvalue of alpha
    matched_num=(pvalues>CRITIC).sum()

    return matched_num

def _for_one_combination(args):
    _names,simulated_factors=args
    model_factor_names = ['const', 'rp'] + list(_names)
    model = np.matrix(simulated_factors[model_factor_names])#trick: matrix
    assets = np.matrix(simulated_factors.drop(model_factor_names, axis=1)) #trick: matrix
    return _names,get_matched_number(model,assets)

def get_data():
    benchmark=pd.read_pickle(os.path.join(DIR,'benchmark.pkl'))
    raw_factors=pd.read_pickle(os.path.join(DIR,'raw_factors.pkl'))
    # benchmark=pd.read_pickle(r'E:\tmp_kogan\benchmark.pkl')
    # raw_factors=pd.read_pickle(r'E:\tmp_kogan\raw_factors.pkl')
    return benchmark,raw_factors

def match_with_all_possible_three_factor_models(factors):
    '''
    :param factors:DataFrame, factors must contain two columns named ['const','rp']
    :return: MultiIndex Series
    '''
    def args_generator():
        for _names in itertools.combinations([col for col  in factors.columns if col not in ['const', 'rp']], 2):
            yield _names,factors
    results=multi_task(_for_one_combination,args_generator(),6)
    _names_l=[r[0] for r in results]
    _matched_l=[r[1] for r in results]
    index=pd.MultiIndex.from_tuples(_names_l)
    matched_series=pd.Series(_matched_l,index=index)
    return matched_series

def get_realized_result():
    benchmark, raw_factors = get_data()
    raw_factors['rp']=benchmark['rp']
    raw_factors['const']=1
    realized=match_with_all_possible_three_factor_models(raw_factors)
    realized.to_pickle(os.path.join(DIR,'realized.pkl'))

# if __name__ == '__main__':
#     get_realized_result()



def simulate_onetime(_id,benchmark,raw_factors,realized_result,anomaly_num):
    simulated_factors = bootstrap_kogan(benchmark, raw_factors, realized_result,
                                        anomaly_num)
    simulated_factors = sm.add_constant(simulated_factors)
    # def args_generator():
    #     for _names in itertools.combinations([col for col  in simulated_factors.columns if col not in ['const', 'rp']], 2):
    #         yield _names,simulated_factors
    return match_with_all_possible_three_factor_models(simulated_factors)

    # results=multi_task(_for_one_combination,args_generator(),6)
    # # results=[_for_one_combination(args) for args in args_generator()]
    # _names_l=[r[0] for r in results]
    # _matched_l=[r[1] for r in results]
    # index=pd.MultiIndex.from_tuples(_names_l)
    # matched_series=pd.Series(_matched_l,index=index)
    # print(_id)
    # return matched_series

def simulate(sim_num=10,anomaly_num=0):
    benchmark, raw_factors = get_data()
    realized_result = pricing_assets(benchmark, raw_factors)
    ss=[simulate_onetime(i,benchmark,raw_factors,realized_result,anomaly_num) for i in range(sim_num)]
    df=pd.concat(ss,axis=1)
    df.to_pickle(os.path.join(DIR,f'{anomaly_num}_{sim_num}.pkl'))
    # df.to_pickle(r'E:\tmp_kogan\{}_{}.pkl'.format(anomaly_num,sim_num))

def run():
    for anomaly_num in [60,110]:#fixme:
        simulate(sim_num=100,anomaly_num=anomaly_num)
        print(anomaly_num)

def get_fig5():
    '''Fig5'''
    ans=[0, 10, 50,60,100,110, 150, 194]
    ss=[]
    for an in ans:
        # s=pd.read_pickle(r'e:\tmp_kogan\{}_100.pkl'.format(an)).stack()
        df=pd.read_pickle(os.path.join(DIR,f'{an}_100.pkl'))
        s = df.apply(lambda s: s.value_counts() / len(s)).reindex(index=range(1, 194)).fillna(0).mean(axis=1)
        s.name=an
        ss.append(s)
        print(an)
    realized = pd.read_pickle(os.path.join(DIR, 'realized.pkl'))
    realized=realized.value_counts()/len(realized)
    realized=realized.reindex(index=range(194))
    realized.name='realized'
    comb=pd.concat(ss+[realized],axis=1)
    # comb.plot.kde(bw_method=0.3).get_figure().savefig(os.path.join(DIR,'distribution_all.pdf'))
    comb.plot().get_figure().savefig(os.path.join(DIR,'distribution_all.pdf'))

