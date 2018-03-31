#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
import os


import statsmodels.api as sm
import numpy as np
import scipy.optimize as opt


def sz50_constitute():
    path=r'C:\data\sz50'
    data=w.wset("sectorconstituent","date=2016-04-01;windcode=000016.SH")
    df=pd.DataFrame(data.Data,index=['time','code','name'])
    df=df.T
    df=df.set_index('code')
    del df['time']
    df.to_csv(os.path.join(path,'2016-04-01.csv'),encoding='gbk')

def construct_cross_sectional_data():
    risk_free=0.04/12
    industry=pd.read_csv(r'c:\data\sz50\sz50.csv',index_col=0)
    bp=pd.read_csv(r'C:\data\barra_factors_combined\BP\2016-03-31.csv',index_col=0)
    size=pd.read_csv(r'C:\data\barra_factors\market_value\2016-03-31.csv',index_col=0)
    normalized_size=pd.read_csv(R'C:\data\barra_factors_combined\market_value\2016-03-31.csv',index_col=0)
    weights=np.sqrt(size) #TODO:to use the reciprocal square root
    # weights=1000/weights
    returns=pd.read_csv(r'C:\data\barra_factors_combined\month_returns\2016-04-30.csv',index_col=0)
    cross_df=industry.copy()
    cross_df=cross_df.fillna(0)
    cross_df['BP']=bp.iloc[:,0]
    cross_df['size']=normalized_size.iloc[:,0]
    cross_df['weights']=weights.iloc[:,0]
    cross_df['returns']=returns.iloc[:,0]-risk_free
    cross_df['fc']=1
    cross_df=cross_df.dropna(axis=0)
    cross_df.to_csv(r'c:\data\sz50\cross_df.csv')
    return cross_df

df=construct_cross_sectional_data()
# df=pd.read_csv(r'c:\data\sz50\cross_df.csv',index_col=0)
factors=['fc','BP','size','bank','non_bank','other']

total_size=[]
for industry_factor in factors[3:]:
    s=df[df[industry_factor]==1.0]['size'].sum()
    total_size.append(s/1000000)

r=np.mat(df['returns']).T
X=np.mat(df[factors])
W=np.mat(np.diag(df['weights']))

factors_weights=(X.T*W*X).I*X.T*W
factors_weights=pd.DataFrame(factors_weights,index=factors,columns=df.index)
factors_weights=factors_weights.T
factors_weights['name']=df['name']
factors_weights.to_csv(R'C:\data\sz50\factors_weights.csv')



industry_w=np.array(total_size)
industry_w=industry_w/industry_w.sum()

times=[0]

def min_func(beta):
    # beta=np.zeros((6,1))
    beta=np.mat(beta).T
    error=(r-X*beta).T*W*(r-X*beta)
    times[0]+=1
    print times[0],error[0,0],beta[3:].flatten()
    return error[0,0]  #notice that slicing in a matrix is different from that in array or list


# cons=({'type':'ineq','fun':lambda beta:0.000001-np.dot(industry_w,beta[3:])})
cons=({'type':'eq','fun':lambda beta:np.dot(industry_w,beta[3:])})
beta0=np.zeros(6)
result=opt.minimize(min_func,beta0,constraints=cons,options={'maxiter':20,'disp':True})
# result=opt.minimize(min_func,np.ones((6,1)),method='SLSQP',constraints=cons,options={'maxiter':1000,'disp':True})

#TODO:print the information of iterations


#method2----------------------------------------------------
# r=np.mat(df['returns']).T
# X=np.mat(df[factors])
# W=np.mat(np.diag(df['weights']))
# combination2=(X.T*W*X).I*X.T*W
# factor_returns2=combination2*r
# df2=pd.DataFrame(combination2.T,index=df.index,columns=factors)
# df2=df2[['fc','bank','non_bank','other','BP','size']]
# df2.to_csv(r'c:\data\sz50\df2.csv')

# X=np.array(df[factors])
# y=np.array(df['returns']).reshape((len(df['returns']),1))
# regression_W=np.diag(df['weights'])
#
# industry_w=np.array(total_size)
# industry_w=industry_w/industry_w.sum()
#
# def min_func(beta):
#     '''
#     y,beta are both column vectors
#     X,W are both matrixes
#     '''
#     error=np.dot(np.dot((y-np.dot(X,beta)).T,regression_W),y-np.dot(X,beta))[0][0]
#     return error
#
# #constraints
# # cons=({'type':'ineq','fun':lambda beta:0.000001-np.dot(industry_w,beta[3:])})
# cons=({'type':'eq','fun':lambda beta:np.dot(np.diag(industry_w),beta[3:]).sum()})
# result=opt.minimize(min_func,np.zeros((6,1)),method='SLSQP',constraints=cons,options={'maxiter':1000,'disp':True})
# # result=opt.minimize(min_func,np.ones((6,1)),method='SLSQP',constraints=cons,options={'maxiter':1000,'disp':True})
#





# method0--------------------------------------------------
# df=construct_cross_sectional_data()
# # df=pd.read_csv(r'c:\data\sz50\cross_df.csv',index_col=0)
# factors=['bank','non_bank','other','BP','size','fc']
# X=df[factors]
# y=df['returns']
# mod=sm.WLS(y,X,weights=df['weights']).fit()
# with open(r'c:\data\sz50\result.txt','w') as f:
#     f.write(mod.summary().as_text())
# factor_returns0=mod.params

#method1--------------------------------------------------
# r=np.array(df['returns'])
# X=np.array(df[factors])
# W=np.diag(df['weights'])
# M1=np.dot(np.dot(X.T,W),X)
# M2=np.dot(np.linalg.inv(M1),X.T)
# combination1=np.dot(M2,W)
# factor_returns1=np.dot(combination1,r)
# df1=pd.DataFrame(combination1.T,index=df.index,columns=factors)
# df1['name']=df['name']
# df1=df1[['fc','bank','non_bank','other','BP','size']]
# df1.to_csv(r'C:\data\sz50\df1.csv')

#method2----------------------------------------------------
# r=np.mat(df['returns']).T
# X=np.mat(df[factors])
# W=np.mat(np.diag(df['weights']))
# combination2=(X.T*W*X).I*X.T*W
# factor_returns2=combination2*r
# df2=pd.DataFrame(combination2.T,index=df.index,columns=factors)
# df2=df2[['fc','bank','non_bank','other','BP','size']]
# df2.to_csv(r'c:\data\sz50\df2.csv')



























