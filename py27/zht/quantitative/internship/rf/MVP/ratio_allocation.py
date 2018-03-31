#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as scs



df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
stock_name=['300296.SZ','600570.SS','002643.SZ']
noa=len(stock_name)

stock=df.loc[:,stock_name]
stock.hist(bins=50)

def print_statistics(arr):
    sta=scs.describe(arr)
    print '%14s %15s'%('statistic','value')
    print 30*'-'
    print '%14s %15d' % ('size',sta[0])
    print '%14s %15.5f' % ('min',sta[1][0])
    print '%14s %15.5f' % ('max', sta[1][1])
    print '%14s %15.5f' % ('mean', sta[2])
    print '%14s %15.5f' % ('std', sta[3])
    print '%14s %15.5f' % ('skew', sta[4])
    print '%14s %15.5f' % ('kurtosis', sta[5])

for sn in stock_name:
    print '\nResults for stock %s'%sn
    print 30*'-'
    ret=np.array(stock[sn].dropna())
    print_statistics(ret)

for sn in stock_name:
    ret=np.array(stock[sn].dropna())
    sm.qqplot(ret,line='s')


def normality_test(arr):
    '''
    给定的数据集进行正态性检验
    组合了3种统计学测试
    偏度测试——足够接近0
    峰度测试——足够接近0
    正态性测试
    :param arr:
    :return:
    '''
    print 'skew of data set %15.3f'%scs.skew(arr)
    print 'kurt of data set %15.3f'%scs.kurtosis(arr)
    print 'skew test p-value %14.3f' % scs.skewtest(arr)[1]
    print 'kurt test p-value %14.3f'%scs.kurtosistest(arr)[1]
    print 'norm test p-value %14.3f'%scs.normaltest(arr)[1]

for sn in stock_name:
    print '\nResults for stock %s'%sn
    print 30*'-'
    ret=np.array(stock[sn].dropna())
    normality_test(ret)

# count=stock.count(axis=1)
# for i in range(len(count)):
#     if count.values[i]==3:
#         print count.index[i]
#         print i
#         break
tmp_stock=stock.copy()
tmp_stock=tmp_stock.iloc[1789:,:]

def change_index_format(dataframe):
    ind=list([str(m) for m in dataframe.index])
    new_ind=[d[:4]+'-'+d[4:6]+'-'+d[6:] for d in ind]
    dataframe.index=[pd.Timestamp(nd) for nd in new_ind]

change_index_format(tmp_stock)
tmp_stock.iloc[0,:]=0.0
tmp_stock=tmp_stock.fillna(0.0)
tmp_stock.cumsum().plot()

'''
# tmp_stock=tmp_stock.dropna(axis=0,how='any')
tmp_stock.mean()*252
tmp_stock.cov()*252

weights=np.random.random(noa)
weights/=np.sum(weights)
print weights

np.sum(tmp_stock.mean()*weights)*252

np.dot(weights.T,np.dot(tmp_stock.cov()*252,weights))

np.sqrt(np.dot(weights.T,np.dot(tmp_stock.cov()*252,weights)))
'''

port_returns=[]
port_variance=[]
for p in range(4000):
    weights=np.random.random(noa)
    weights/=np.sum(weights)
    port_returns.append(np.sum(tmp_stock.mean()*252*weights))
    port_variance.append(np.sqrt(np.dot(weights.T,np.dot(tmp_stock.cov()*252,weights))))

port_returns=np.array(port_returns)
port_variance=np.array(port_variance)

risk_free=0.04
plt.figure(figsize=(8,4))
plt.scatter(port_variance,port_returns,c=(port_returns-risk_free)/port_variance,marker='o')
plt.grid(True)
plt.xlabel('excected volatility')
plt.ylabel('expected return')
plt.colorbar(label='sharpe ratio')

def statistics(weights):
    weights=np.array(weights)
    port_returns=np.sum(tmp_stock.mean()*weights)*252
    port_variance=np.sqrt(np.dot(weights.T,np.dot(tmp_stock.cov()*252,weights)))
    return np.array([port_returns,port_variance,port_returns/port_variance])

import scipy.optimize as sco

def min_sharpe(weights):
    return -statistics(weights)[2]

cons=({'type':'eq','fun':lambda x:np.sum(x)-1})
bnds=tuple((0,1) for x in range(noa))

opts=sco.minimize(min_sharpe,np.array([1.0/noa]*noa),method='SLSQP',bounds=bnds,constraints=cons)
statistics(opts['x'])


def min_variance(weights):
    return statistics(weights)[1]

optv=sco.minimize(min_variance,np.array([1.0/noa]*noa),method='SLSQP',bounds=bnds,constraints=cons)
statistics(optv['x'])


def min_variance(weights):
    return statistics(weights)[1]

target_returns=np.linspace(0.45,0.6,50)
target_variance=[]
for tar in target_returns:
    cons=({'type':'eq','fun':lambda x:statistics(x)[0]-tar},{'type':'eq','fun':lambda x:np.sum(x)-1})
    res=sco.minimize(min_variance,np.array(noa*[1./noa]),method='SLSQP',bounds=bnds,constraints=cons)
    target_variance.append(res['fun'])

target_variance=np.array(target_variance)

plt.figure(figsize=(8,4))
plt.scatter(port_variance,port_returns,c=port_returns/port_variance,marker='o')
plt.scatter(target_variance,target_returns,c=target_returns/target_variance,marker='x')
plt.plot(statistics(opts['x'])[1],statistics(opts['x'])[0],'r*',markersize=15)
plt.plot(statistics(optv['x'])[1],statistics(optv['x'])[0],'y*',markersize=15)
plt.grid(True)
plt.xlabel('excected volatility')
plt.ylabel('expected return')
plt.colorbar(label='sharpe ratio')

