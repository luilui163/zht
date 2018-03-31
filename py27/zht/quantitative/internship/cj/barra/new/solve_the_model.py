#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
from zht.data import data_handler
from zht.data import file_handler
import os
import statsmodels.api as sm
from tool import mark
import scipy.optimize as opt
import matplotlib.pyplot as plt
from matplotlib.dates import date2num


@mark
def tvalue():
    filepath=r'C:\data\barra_cross_data\2016-06-30.csv'
    df=pd.read_csv(filepath,index_col=0)
    factors=[col for col in df.columns if col!='weights' and col!='month_returns'and col!='fc' and col!='size']

    path=r'C:\data\barra_cross_data'
    filenames=os.listdir(path)
    tvalue_df=pd.DataFrame()
    for filename in filenames:
        date=filename[:-4]
        df=pd.read_csv(os.path.join(path,filename),index_col=0)
        y=df['month_returns']
        for factor in factors:
            X=df[factor]
            X=sm.add_constant(X)
            mod=sm.WLS(y,X,weights=df['weights']).fit()
            tvalue=mod.tvalues[1]
            tvalue_df.at[date,factor]=tvalue
    mean=abs(tvalue_df).mean()
    ratio=tvalue_df[abs(tvalue_df)>2].count()/len(tvalue_df)
    summary_df=pd.DataFrame()
    summary_df['mean']=mean
    summary_df['ratio']=ratio
    # summary_df.to_csv(r'C:\data\result\tvalue.csv')

@mark
# def get_cross_sectional_corr():
#     path=r'C:\data\barra_factors_combined'
#     directorys=os.listdir(path)
#     date_intersection=file_handler.get_date_intersection(path)
#     for date in date_intersection:
#         df=pd.DataFrame()
#         for directory in directorys:
#             if directory not in ['industry','weights','month_returns','size']:
#                 sub_df=pd.read_csv(os.path.join(path,directory,date+'.csv'),index_col=0)
#                 df[directory]=sub_df.iloc[:,0]
#         corr_df=df.corr()
#         corr_df.to_csv(r'C:\data\result\corr\%s.csv'%date)

@mark
# def get_avg_corr():
#     path=r'C:\data\result\corr'
#     filenames=os.listdir(path)
#     df=pd.read_csv(os.path.join(path,filenames[0]),index_col=0)
#     for filename in filenames[1:]:
#         sub_df=pd.read_csv(os.path.join(path,filename),index_col=0)
#         df+=sub_df
#     df=df/len(filenames)
#     df.to_csv(r'C:\data\result\corr_avg.csv')

@mark
def vif():
    path=r'C:\data\barra_factors_combined'
    directorys=os.listdir(path)
    factors=[d for d in directorys if d!='industry' and d!='month_returns' and d!='weights']
    date_intersection=file_handler.get_date_intersection(path)
    vif=pd.DataFrame()
    for date in date_intersection:
        df=pd.DataFrame()
        for factor in factors:
            sub_df=pd.read_csv(os.path.join(path,factor,date+'.csv'),index_col=0)
            df[factor]=sub_df.iloc[:,0]
        df=df.drop(df[pd.isnull(df[factor])].index)
        df=df.dropna(axis=0,thresh=len(factors)-3)
        df=df.fillna(0)
        for factor in factors:
            y=df[factor]
            X=df[[f for f in factors if f!=factor]]
            X=sm.add_constant(X)
            mod=sm.OLS(y,X).fit()
            vif.at[date,factor]=1.0/(1-mod.rsquared)
    vif_mean=pd.DataFrame()
    vif_mean['mean']=vif.mean()
    vif.to_csv(r'C:\data\result\vif.csv')
    vif_mean.to_csv(r'c:\data\result\vif_mean.csv')

@mark
def get_factor_returns():
    filepath = r'C:\data\barra_cross_data\2016-06-30.csv'
    df = pd.read_csv(filepath, index_col=0)
    factors = [col for col in df.columns if col != 'weights' and col != 'month_returns'and col!='size']

    path = r'C:\data\barra_cross_data'
    filenames = os.listdir(path)
    factor_returns = pd.DataFrame(index=factors)
    for filename in filenames:
        date = filename[:-4]
        df = pd.read_csv(os.path.join(path, filename), index_col=0)
        # y = df['month_returns']
        # X=df[factors]
        # mod = sm.WLS(y, X, weights=df['weights']).fit()

        r=np.mat(df['month_returns']).T
        X=np.mat(df[factors])
        W=np.mat(np.diag(df['weights']/df['weights'].sum())) #TODO:是的w的和为1？

        factors_weights = (X.T * W * X).I * X.T * W
        factors_weights = pd.DataFrame(factors_weights, index=factors, columns=df.index)
        factors_weights = factors_weights.T
        factors_weights.to_csv(R'C:\data\result\factors_weights\%s.csv'%date)

        industry_names=[col for col in df.columns if col.startswith('SW')]
        industry_index=[list(df.columns).index(industry_name) for industry_name in industry_names]
        total_size=[]
        for industry_name in industry_names:
            s=df[df[industry_name]==1.0]['size'].sum()
            total_size.append(s/1000) #scale down the numbers,this doesn't affect the result
        industry_w = np.array(total_size)
        industry_w = industry_w / industry_w.sum()

        ###########################
        def min_func(beta):
            beta = np.mat(beta).T
            error = (r - X * beta).T * W * (r - X * beta)
            return error[0, 0]  # notice that slicing in a matrix is different from that in array or list

        cons = ({'type': 'eq', 'fun': lambda beta: np.dot(industry_w, beta[industry_index])})
        beta0 = np.ones(len(factors))
        result = opt.minimize(min_func, beta0, method='SLSQP',constraints=cons)

        factor_returns[date]=result.x
        ##################################
        print filename,result.fun

    factor_returns=factor_returns.T
    style_factors=[f for f in factors if not f.startswith('SW')]
    industry_factors=[f for f in factors if f.startswith('SW')]
    style_df=factor_returns[style_factors]
    industry_df=factor_returns[industry_factors]

    ax=style_df.cumsum().plot()
    fig=ax.get_figure()
    fig.savefig(r'C:\data\result\style.png')

    ax=industry_df.cumsum().plot()
    fig=ax.get_figure()
    fig.savefig(r'C:\data\result\industry.png')

    style_df.to_csv(r'c:\data\result\style_returns.csv')
    industry_df.to_csv(r'c:\data\result\industry_returns.csv')

def get_style_corr():
    style_returns=pd.read_csv(R'c:\data\result\style_returns.csv',index_col=0)
    style_corr=style_returns.corr()
    style_corr.to_csv(r'c:\data\result\style_corr.csv')

def summary():
    summary=pd.DataFrame()
    style_returns=pd.read_csv(r'c:\data\result\style_returns.csv',index_col=0)
    return_monthly=style_returns.mean()
    return_yearly=return_monthly*12
    std_monthly=style_returns.std()
    std_yearly=std_monthly*pow(12,0.5)
    summary['return_yearly']=return_yearly
    summary['std_yearly']=std_yearly
    summary['return/risk']=abs(return_yearly)/std_yearly
    summary=summary.drop('fc')
    summary.to_csv(r'c:\data\result\summary.csv')

def get_figure():
    style_returns=pd.read_csv(R'C:\data\result\style_returns.csv',index_col=0)
    summary=pd.read_csv(R'C:\data\result\summary.csv',index_col=0)
    factors=list(summary.index)
    direction=np.sign(summary['return_yearly'])
    direction=dict(direction)

    for factor in factors:
        s=style_returns[factor]*direction[factor]
        s=s+1
        s=s.cumprod()

        plt.rc('axes',grid=True)
        plt.rc('grid',color='0.75',linestyle='-',linewidth=0.5)

        textsize=9
        left,width=0.1,0.8
        rect=[left,left,width,width]

        fig=plt.figure(facecolor='white',figsize=(16,9))
        axescolor='#f6f6f6'
        ax=fig.add_axes(rect,axisbg=axescolor)
        axt=ax.twinx()

        index=[pd.to_datetime(ind) for ind in s.index]
        ax.bar(index,style_returns[factor])
        axt.plot(index,s.values)
        fig.savefig(r'C:\data\result\figure\%s.png'%factor)

def run():
    get_factor_returns()
    get_style_corr()
    summary()
    get_figure()

if __name__=='__main__':
    run()

#TODO:change different initial value,this doesn't matter

#TODO:权重是否需要使他们的和为1，看一下WLS的源代码
#TODO:分析factors return
#TODO:绘图分析factor returns的月收益 bar图，2，r-X*result.x 差距很大。








