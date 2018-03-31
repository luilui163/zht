#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
import construct_cross_sectional
import scipy.optimize as opt

def tvlue():
    filepath=r'C:\data\zz800\cross_df.csv'
    df=pd.read_csv(filepath,index_col=0)
    factors=[col for col in df.columns if col not in ['pct_chg']]

    y=df['pct_chg']
    for factor in factors:
        X=df[factor]
        X['constant']=1
        W = construct_cross_sectional.get_weight_matrix()
        b=(X.T*W*X).I*X.T*W*y #the slope
        TSS=(y-W*y).T*W*(y-W*y)
        RSS=(y-X*b).T*W*(y-X*b)
        rsqure=1-RSS/TSS #refer to https://www.codeproject.com/articles/25335/an-algorithm-for-weighted-linear-regression


def solve():
    df=pd.read_csv(R'C:\data\zz800\cross_df.csv',index_col=0)
    style_factors=['benchmark_return','turnover']
    sector_factors=[col for col in df.columns if col not in ['pct_chg','turnover','benchmark_return']]
    factors=style_factors+sector_factors

    r=np.mat(df['pct_chg']).T
    X=np.mat(df[factors])
    W=construct_cross_sectional.get_weight_matrix()

    factor_weights = (X.T * W * X).I * X.T * W
    factor_returns=factor_weights*r

    #save factor_weights as df
    factor_weights = pd.DataFrame(factor_weights, index=factors, columns=df.index)
    factor_weights = factor_weights.T
    factor_weights.to_csv(R'C:\data\zz800\factor_weights.csv')
    #save factor_returns as df
    factor_returns=pd.DataFrame(factor_returns,index=factors,columns=['returns'])
    factor_returns.to_csv(r'c:\data\zz800\factor_returns.csv')


def optimization():
    def min_func(beta):
        beta = np.mat(beta).T
        error = (r - X * beta).T * W * (r - X * beta)
        return error[0, 0]  # notice that slicing in a matrix is different from that in array or list




if __name__=='__main__':
    solve()



#TODO:加入限制条件










