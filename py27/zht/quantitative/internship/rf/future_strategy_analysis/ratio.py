import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


corr=pd.read_csv('corr.csv',index_col=0)
pf=pd.read_csv('performance.csv',index_col=0)


port_returns = []
port_variance = []
port_mmd=[]
for p in range(1000):
    weights = np.random.random(len(corr))
    weights /=np.sum(weights)
    port_returns.append(np.sum(pf['returns']*weights))
    port_variance.append(np.sqrt(np.dot(weights.T, np.dot(np.array(corr), weights))))
    port_mmd.append(np.sum(pf['max_drawdown']*weights))
    print p

port_returns = np.array(port_returns)
port_variance = np.array(port_variance)

#无风险利率设定为4%
risk_free = 0.04
plt.figure(figsize = (8,4))
plt.scatter(port_variance, port_returns, c=(port_returns-risk_free)/port_mmd, marker = 'o')
plt.grid(True)
plt.xlabel('excepted max_drawdown')
plt.ylabel('expected return')
plt.colorbar(label = 'A')

def statistics(weights):
    weights=np.array(weights)
    port_returns=np.sum(pf['returns']*weights)
    port_mmd=np.sum(pf['max_drawdown']*weights)
    return np.array([port_returns,port_mmd,(port_returns-0.02)/port_mmd])

import scipy.optimize as sco

def min_A(weights):
    return -statistics(weights[2])

cons=({'type':'eq','fun':lambda x:np.sum(x)-1})

bnds=tuple((0,1) for x in range(len(corr)))

opts=sco.minimize(min_A,np.array(10*[0.1]),method='SLSQP',bounds=bnds,constraints=cons)
opts['x']






