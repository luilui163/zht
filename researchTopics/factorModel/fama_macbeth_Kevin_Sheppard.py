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



# Moment conditions
X = hstack((ones((T, 1)), factors))
p = vstack((alpha, beta))
epsilon = excessReturns - X * p
moments1 = kron(epsilon, ones((1, K + 1)))
moments1 = multiply(moments1, kron(ones((1, N)), X))
u = excessReturns - riskPremia.T * beta
moments2 = u * beta.T
# Score covariance
S = mat(cov(hstack((moments1, moments2)).T))
# Jacobian
G = mat(zeros((N * K + N + K, N * K + N + K)))
SigmaX = X.T * X / T
G[:N * K + N, :N * K + N] = kron(eye(N), SigmaX)
G[N * K + N:, N * K + N:] = -beta * beta.T
for i in xrange(N):
    temp = zeros((K, K + 1))
    values = mean(u[:, i]) - multiply(beta[:, i], riskPremia)
    temp[:, 1:] = diag(values.A1)
    G[N * K + N:, i * (K + 1):(i + 1) * (K + 1)] = temp

vcv = inv(G.T) * S * inv(G) / T

vcvAlpha = vcv[0:N * K + N:4, 0:N * K + N:4]
J = alpha * inv(vcvAlpha) * alpha.T
J = J[0, 0]
Jpval = 1 - chi2(25).cdf(J)


vcvRiskPremia = vcv[N * K + N:, N * K + N:]
annualizedRP = 12 * riskPremia
arp = list(squeeze(annualizedRP.A))
arpSE = list(sqrt(12 * diag(vcvRiskPremia)))
print('        Annualized Risk Premia')
print('           Market       SMB        HML')
print('--------------------------------------')
print('Premia     {0:0.4f}    {1:0.4f}     {2:0.4f}'.format(arp[0], arp[1], arp[2]))
print('Std. Err.  {0:0.4f}    {1:0.4f}     {2:0.4f}'.format(arpSE[0], arpSE[1], arpSE[2]))
print('\n\n')

print('J-test:   {:0.4f}'.format(J))
print('P-value:   {:0.4f}'.format(Jpval))




i = 0
betaSE = []
for j in xrange(5):
    for k in xrange(5):
        a = alpha[0, i]
        b = beta[:, i].A1
        variances = diag(vcv[(K + 1) * i:(K + 1) * (i + 1), (K + 1) * i:(K + 1) * (i + 1)])
        betaSE.append(sqrt(variances))
        s = sqrt(variances)
        c = hstack((a, b))
        t = c / s
        print('Size: {:}, Value:{:}   Alpha   Beta(VWM)   Beta(SMB)   Beta(HML)'.format(j + 1, k + 1))
        print('Coefficients: {:>10,.4f}  {:>10,.4f}  {:>10,.4f}  {:>10,.4f}'.format(a, b[0], b[1], b[2]))
        print('Std Err.      {:>10,.4f}  {:>10,.4f}  {:>10,.4f}  {:>10,.4f}'.format(s[0], s[1], s[2], s[3]))
        print('T-stat        {:>10,.4f}  {:>10,.4f}  {:>10,.4f}  {:>10,.4f}'.format(t[0], t[1], t[2], t[3]))
        print('')
        i += 1

betaSE = array(betaSE)
savez_compressed('Fama-MacBeth_results', alpha=alpha, \
                 beta=beta, betaSE=betaSE, arpSE=arpSE, arp=arp, J=J, Jpval=Jpval)