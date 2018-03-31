#-*-coding: utf-8 -*-
#author:tyhj
#fama_macbeth_Kevin_Sheppard.py 2017.10.15 17:27


from __future__ import division
from numpy import mat, cov, mean, hstack, multiply,sqrt,diag, genfromtxt, \
    squeeze, ones, array, vstack, kron, zeros, eye, savez_compressed
from numpy.linalg import lstsq, inv
from scipy.stats import chi2
from pandas import read_csv


data=read_csv('FamaFrench.csv')
dates=data['date'].values
factors=data[['VWMe','SMB','HML']].values
rf=data['RF'].values
portfolios=data.ix[:,5:].values

factors=mat(factors)
rf=mat(rf)
portfolios=mat(portfolios)

T,K=factors.shape
T,N=portfolios.shape

rf.shape=T,1
excessReturns=portfolios-rf

#time series regressions
X=hstack((ones((T,1)),factors))
out=lstsq(X,excessReturns)

alpha=out[0][0]
beta=out[0][1:]

avgExcessReturns=mean(excessReturns,0)

#cross-section regression
out=lstsq(beta.T,avgExcessReturns.T)
riskPremia=out[0]




