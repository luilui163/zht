#-*-coding: utf-8 -*-
#author:tyhj
#tools.py 2017/9/19 11:48
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



from zht.util.statu import GRS_test
from zht.util import pandasu




from params import *


def getIndicatorId(indicator,param):
    '''

    :param indicator:str, name of indicator
    :param param:
    :return: pandas.Dataframe,the index is month series
    '''
    df=pd.read_csv(os.path.join(idp,indicator+'.csv'),index_col=0)
    id=pandasu.getSortedPortId(df,param)
    newIndex = pd.date_range(start=id.index[0], end=str(int(id.index[-1][:4]) + 1) + '-07', freq='M')
    newIndex = [ind.strftime('%Y-%m') for ind in newIndex]
    id = id.reindex(index=newIndex)
    id = id.shift(1)
    id = id.ffill()
    return id

def calPortRet(portId):
    '''
    monthly,calculate weighted return and the weight is market value

    Args:
        portId: dataframe with index as timestamp like '2012-12'
    Returns:

    '''

    ret = pd.read_csv(os.path.join(bdp, 'ret.csv'), index_col=0)
    weight = pd.read_csv(os.path.join(bdp, 'weight.csv'), index_col=0)
    ports = np.sort([p for p in np.unique(portId.fillna(0.0)) if p!=0.0])

    portId,ret,weight=pandasu.get_inter_frame([portId,ret,weight])

    portRet = pd.DataFrame(index=portId.index, columns=ports)

    for month in portId.index.tolist():
        for port in ports:
            stocks=portId.columns[portId.loc[month]==port].tolist()
            try:
                tmp=pd.DataFrame()
                tmp['ret']=ret.loc[month,stocks]
                tmp['weight']=weight.loc[month,stocks]
                tmp=tmp.dropna(axis=0,how='any')
                pr=pandasu.mean_self(tmp,'ret','weight')
                portRet.loc[month,port]=pr
            except KeyError:
                pass
        print month
    return portRet

def intersectionFactorRet(vars,model):
    '''
    sort independently,high id minus low id,market value weighted in each port,equally weighted
    between different ports.

    Args:
        vars:list or tuple
        model: '2x2','2x3','3x2','3x3','2x2x2','2x3x3','2x2x2x2',and so on.

    Returns:
        pd.Series

    '''
    ns = model.split('x')
    idList = []
    for i in range(len(vars)):
        id = getIndicatorId(vars[i], int(ns[i]))
        # id = pd.read_csv(os.path.join(idip, ns[i], vars[i] + '.csv'), index_col=0)
        idList.append(id)
    idList = pandasu.get_inter_frame(idList)

    portId = pd.DataFrame(0, index=idList[0].index, columns=idList[0].columns)
    for j in range(len(idList)):
        portId += idList.pop() * pow(10, j)

    portRet = calPortRet(portId)

    pns = portRet.columns.tolist()

    factorList = []
    for m, var in enumerate(vars):
        highCols = [p for p in pns if str(p)[m] == ns[m]]
        lowCols = [p for p in pns if str(p)[m] == '1']
        factorList.append(portRet[highCols].mean(axis=1) - portRet[lowCols].mean(axis=1))

    return tuple(factorList)

def buildModel(vars,model):
    '''
    :param vars:
    :param model:
    :return:
    '''
    factors=intersectionFactorRet(vars,model)
    iv=pd.DataFrame()
    iv['rp']=pd.read_csv(os.path.join(bdp,'rp.csv'),index_col=0)['rp']
    for i,factor in enumerate(factors):
        iv[vars[i]]=factor
    return iv


#TODO:sort combined,rather than independently


def regressBenchmark(dvdf,model):
    '''
    regress on the base model to calculate various indicators,such as alpha,coeffient,t,r2,GRS,GRS pvalue.

    Args:
        dvdf: pandas dataframe,dependent variable dataframe.For each column,
              there a time series of return for one group.The whole dataframe
              stores all the return of the portfolios.
        model: 'capm','ff3','carhart4','liq4','ff5'

    Returns:
        COEF, T, R2, RESID:dataframe
        GRS,GRSp:float value

    '''
    iv=pd.DataFrame()
    if model in ['capm','ff3','carhart4','liq4','ff5','hxz4']:
        iv=pd.read_csv(os.path.join(bmp,model+'.csv'),index_col=0)


    dv = dvdf.dropna(axis=0, how='any')
    iv = iv.dropna(axis=0, how='any')

    iv, dv = pandasu.get_inter_index([iv, dv])

    COEF = pd.DataFrame(columns=['constant'] + iv.columns.tolist())
    T = pd.DataFrame(columns=['constant'] + iv.columns.tolist())
    R2 = pd.DataFrame(columns=['r2'])
    RESID = pd.DataFrame()

    for col in dv.columns.tolist():
        df = pd.DataFrame()
        df[col] = dv[col]
        df[iv.columns.tolist()] = iv
        if df.shape[0] > iv.shape[1] + 1:  # make sure that the number of samples is larger than the number of factors plus one.
            coef, t, r2, resid = pandasu.reg(df)
            COEF.loc[col] = coef
            T.loc[col] = t
            R2.loc[col] = r2
            RESID[col] = pd.Series(resid, index=df.index)

    alpha = np.mat(COEF['constant']).T
    factor = iv.as_matrix()
    GRS, GRSp = GRS_test(factor, RESID.as_matrix(), alpha)

    return COEF, T, R2, RESID, GRS, GRSp


def estimateAlpha(dvdf,model):
    if model in ['capm','ff3','carhart4','liq4','ff5','hxz4']:
        iv=pd.read_csv(os.path.join(bmp,model+'.csv'),index_col=0)
    else:#TODO:new model path is mdp.
        iv=pd.read_csv(os.path.join(mdp,model+'.csv'),index_col=0)

    dvdf['10-1']=dvdf.iloc[:,-1]-dvdf.iloc[:,0]

    dv=dvdf.dropna(axis=0,how='any')
    iv=iv.dropna(axis=0,how='any')

    iv,dv=pandasu.get_inter_index([iv,dv])

    ALPHA=pd.DataFrame(index=dv.columns,columns=[model])
    ALPHAT=pd.DataFrame(index=dv.columns,columns=[model])
    for col in dv.columns:
        df=pd.DataFrame()
        df[col]=dv[col]
        df[iv.columns.tolist()]=iv
        if df.shape[0] > iv.shape[1] + 1:  # make sure that the number of samples is larger than the number of factors plus one.
            coef, t, r2, resid = pandasu.reg(df)
            ALPHA.loc[col,model]=coef[0]
            ALPHAT.loc[col,model]=t[0]
    return ALPHA,ALPHAT

def _reg(df,model):
    if model in ['capm','ff3','carhart4','liq4','ff5','hxz4']:
        slope, t, r2, resid, grs, grsp = regressBenchmark(df, model)
        return slope, t, r2, resid, grs, grsp
    else:
        iv = pd.read_csv(os.path.join(rdmp, model + '.csv'), index_col=0)
        dv = df.dropna(axis=0, how='any')
        iv = iv.dropna(axis=0, how='any')

        iv, dv = pandasu.get_inter_index([iv, dv])

        COEF = pd.DataFrame(columns=['constant'] + iv.columns.tolist())
        T = pd.DataFrame(columns=['constant'] + iv.columns.tolist())
        R2 = pd.DataFrame(columns=['r2'])
        RESID = pd.DataFrame()

        for col in dv.columns.tolist():
            df = pd.DataFrame()
            df[col] = dv[col]
            df[iv.columns.tolist()] = iv
            if df.shape[0] > iv.shape[1] + 1:  # make sure that the number of samples is larger than the number of factors plus one.
                coef, t, r2, resid = pandasu.reg(df)
                COEF.loc[col] = coef
                T.loc[col] = t
                R2.loc[col] = r2
                RESID[col] = pd.Series(resid, index=df.index)

        alpha = np.mat(COEF['constant']).T
        factor = iv.as_matrix()
        GRS, GRSp = GRS_test(factor, RESID.as_matrix(), alpha)

        return COEF, T, R2, RESID, GRS, GRSp

def getValidModels():
    validModels=['capm','ff3','carhart4','liq4','ff5','hxz4']
    fns=os.listdir(mdp)
    for k, fn in enumerate(fns):
        df = pd.read_csv(os.path.join(mdp, fn), index_col=0)
        df = df.dropna(axis=0, how='any')
        #find those models with enough history
        if df.shape[0] > 100:#TODO:set a thresh
            corr = df.corr()
            np.fill_diagonal(corr.values, 0)
            if corr.abs().max().max() < 0.8:  # delete those collinear model
                validModels.append(fn[:-4])
        #TODO:some models may be similar
    return validModels

def regOnAllPossiblemodels():
    grsDf=pd.DataFrame()
    grspDf=pd.DataFrame()

    fns=os.listdir(idrp)

    # filter the model with too short history
    models=getValidModels()

    for n,fn in enumerate(fns):
        df = pd.read_csv(os.path.join(idrp, fn), index_col=0)
        for c,model in enumerate(models):
            dd=os.path.join(regp,fn[:-4])
            dd = dd.replace(' ', '')#There are some space in fn which is invalid character as file name.
            if not os.path.exists(dd):
                os.makedirs(dd)
            slope,t,r2,resid,grs,grsp=_reg(df,model)

            slope.to_csv(os.path.join(dd,'slope_%s.csv'%model))
            t.to_csv(os.path.join(dd,'t_%s.csv'%model))
            r2.to_csv(os.path.join(dd,'r2_%s.csv'%model))
            resid.to_csv(os.path.join(dd,'resid_%s.csv'%model))

            grsDf.loc[fn[:-4],model]=grs
            grspDf.loc[fn[:-4],model]=grsp
            print n,c
    grsDf.to_csv(os.path.join(directory,'grs.csv'))
    grspDf.to_csv(os.path.join(directory,'grsp.csv'))







#============================visualization
def get_3dbar(portEret, var1, var2):
    avg = pd.DataFrame(portEret.mean().values.reshape(5, 5), index=range(1, 6), columns=range(1, 6))
    avg.index.name = var1

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    ax.set_xlabel(var1, )
    ax.set_ylabel(var2)
    ax.set_zlabel("avgEret")
    ax.set_xlim3d(0, 6)
    ax.set_ylim3d(0, 6)

    avg = portEret.mean()
    n = len(avg)

    xpos = [int(float(ind)) / 10 for ind in avg.index]
    ypos = [int(float(ind)) % 10 for ind in avg.index]
    zpos = np.zeros(n)

    dx = np.ones(n) / 4
    dy = np.ones(n) / 4
    dz = avg.values

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='y')

    plt.gca().invert_xaxis()
    plt.show()

    return fig


def get_3dline(portEret, var1, var2):
    # portEret=pd.read_csv(r'D:\quantDb\researchTopics\crossSection\data\portEret.csv',index_col=0)
    avg = pd.DataFrame(portEret.mean().values.reshape(5, 5), index=range(1, 6), columns=range(1, 6))
    X = [[i] * 5 for i in range(1, 6)]
    Y = [range(1, 6) for i in range(5)]
    Z = avg.values

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)

    ax.set_xlabel(var1)
    ax.set_ylabel(var2)
    ax.set_zlabel("avgEret")
    return fig