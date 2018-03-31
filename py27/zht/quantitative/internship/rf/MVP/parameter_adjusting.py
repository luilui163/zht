#-*-coding: utf-8 -*-
#@author:tyhj
'''
parameter1:window length
parameter2:opts or optv or a point between them in the efficient frontier
parameter3:risk_free
            if risk free equals 0,optimize based on IR
parameter3:reblance cycle,can be fixed length or depends on threshhold,
            once some value break up the threshold,we may consider to reblance the
            portfolio weights

contrast with equal weighted portfolio

something to improve:
downside risk
value at risk
chose fluctuation market data to building the model

'''

import scipy.optimize as sco
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as scs


def get_hist_data():
    df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
    stock_name=['300296.SZ','600570.SS','002643.SZ']
    returns=df.loc[:,stock_name].iloc[1800:,:].copy()

    ind=list([str(m) for m in returns.index])
    new_ind=[d[:4]+'-'+d[4:6]+'-'+d[6:] for d in ind]
    returns.index=[pd.Timestamp(nd) for nd in new_ind]
    return returns

returns=get_hist_data()
noa=len(returns.columns)

def get_weights(risk_free,history_window,rebalance_window,count):
    returns_in_window=returns.iloc[count*rebalance_window:history_window+count*rebalance_window,:]

    port_returns=[]
    port_variance=[]
    for p in range(1000):
        weights=np.random.random(noa)
        weights/=np.sum(weights)
        port_returns.append(np.sum(returns_in_window.mean()*252*weights))
        port_variance.append(np.sqrt(np.dot(weights.T,np.dot(returns_in_window.cov()*252,weights))))

    port_returns=np.array(port_returns)
    port_variance=np.array(port_variance)

    def statistics(weights):
        weights=np.array(weights)
        port_returns=np.sum(returns_in_window.mean()*weights)*252
        port_variance=np.sqrt(np.dot(weights.T,np.dot(returns_in_window.cov()*252,weights)))
        return np.array([port_returns,port_variance,(port_returns-risk_free)/port_variance])

    def min_sharpe(weights):
        return -statistics(weights)[2]

    def min_variance(weights):
        return statistics(weights)[1]

    cons=({'type':'eq','fun':lambda x:np.sum(x)-1})
    bnds=tuple((0,1) for x in range(noa))
    opts=sco.minimize(min_sharpe,np.array([1.0/noa]*noa),method='SLSQP',bounds=bnds,constraints=cons)
    optv=sco.minimize(min_variance,np.array([1.0/noa]*noa),method='SLSQP',bounds=bnds,constraints=cons)

    def get_middle_point():
        middle_return=statistics(opts['x'])[0]*0.5+statistics(optv['x'])[0]*0.5
        tmp_cons=({'type':'eq','fun':lambda x:statistics(x)[0]-middle_return},{'type':'eq','fun':lambda x:np.sum(x)-1})
        optm = sco.minimize(min_variance, np.array(noa * [1. / noa]), method='SLSQP', bounds=bnds, constraints=tmp_cons)
        middle_variance=optm['fun']
        return optm['x'],middle_return,middle_variance

    weight_m,middle_return,middle_variance=get_middle_point()
    # weight_s=opts['x'] #something wrong:the ratio between those stocks are extremely biased
    weight_v=optv['x']

    # print count,returns_in_window.index[-1],weight_m,weight_v
    return weight_m,weight_v


def get_fig(history_window,rebalance_window):
    risk_free=0.04
    # history_window=100
    # rebalance_window=30
    count_max=(len(returns)-history_window)/rebalance_window+1

    returns_adjust_df = returns.iloc[history_window:, :]
    weights_m = returns_adjust_df.copy()
    weights_m[weights_m > -1] = np.nan
    weights_v=weights_m.copy()

    for count in range(count_max):
        weight_m, weight_v = get_weights(risk_free, history_window, rebalance_window, count)
        weights_m.iloc[count * rebalance_window, :] = weight_m
        weights_v.iloc[count*rebalance_window,:]=weight_v

    weights_m=weights_m.fillna(method='ffill')
    weights_v=weights_v.fillna(method='ffill')

    # weights_m.to_csv(r'c:\trash\weights_m.csv')

    total_returns_m=returns_adjust_df*weights_m
    total_returns_v=returns_adjust_df*weights_v
    total_returns_a=returns_adjust_df.mean(axis=1)
    total_returns_m=total_returns_m.fillna(0)
    total_returns_v=total_returns_v.fillna(0)
    total_returns_a=total_returns_a.fillna(0)
    pnl_m=total_returns_m.sum(axis=1)
    pnl_v=total_returns_v.sum(axis=1)
    pnl_a=total_returns_a
    pnl_m.values[0]=0.0
    pnl_v.values[0]=0.0
    pnl_a.values[0]=0.0
    pnl_m=pnl_m.cumsum()
    pnl_v=pnl_v.cumsum()
    pnl_a=pnl_a.cumsum()
    pnl_m.name='pnl_m'
    pnl_v.name='pnl_v'
    pnl_a.name='pnl_a'
    pnl_df=pd.concat([pnl_m,pnl_v,pnl_a],axis=1)
    tmp=pnl_df.plot()
    fig=tmp.get_figure()
    fig.savefig(r'c:\trash\fig\{}_{}.png'.format(history_window,rebalance_window))

if __name__=='__main__':
    for history_window in [100]:
        for rebalance_window in [10]:
            get_fig(history_window,rebalance_window)
            print history_window,rebalance_window







