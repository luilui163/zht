#-*-coding: utf-8 -*-
#author:tyhj
#regressionModels.py 2017/9/10 10:24
import pandas as pd
import os
import numpy as np
import time
import itertools
import uuid
from shutil import copyfile


from zht.util import pandasu
from zht.util.statu import GRS_test
from zht.util.mathu import getSortedPortId
from zht.util.listu import chunkify

from params import *
from main import get_portRet

def get_benchmarkModels():
    for model in ['capm', 'ff3', 'carhart4', 'liq4', 'ff5', 'hxz4']:
        iv = pd.DataFrame()

        if model == 'capm':
            iv['rp'] = pd.read_csv(os.path.join(bdp, 'rp.csv'), index_col=0)['rp']
        elif model == 'ff3':
            iv['rp'] = pd.read_csv(os.path.join(bdp, 'rp.csv'), index_col=0)['rp']
            iv['hml'] = pd.read_csv(os.path.join(ff3FactorP, 'hml.csv'), index_col=0)
            iv['smb'] = pd.read_csv(os.path.join(ff3FactorP, 'smb.csv'), index_col=0)
        elif model == 'carhart4':
            iv['rp'] = pd.read_csv(os.path.join(bdp, 'rp.csv'), index_col=0)['rp']
            iv['hml'] = pd.read_csv(os.path.join(ff3FactorP, 'hml.csv'), index_col=0)
            iv['smb'] = pd.read_csv(os.path.join(ff3FactorP, 'smb.csv'), index_col=0)
            iv['carhartMom'] = pd.read_csv(os.path.join(factorRetPath, 'carhartMom.csv'), index_col=0)
        elif model == 'liq4':
            iv['rp'] = pd.read_csv(os.path.join(bdp, 'rp.csv'), index_col=0)['rp']
            iv['hml'] = pd.read_csv(os.path.join(ff3FactorP, 'hml.csv'), index_col=0)
            iv['smb'] = pd.read_csv(os.path.join(ff3FactorP, 'smb.csv'), index_col=0)
            iv['liq'] = pd.read_csv(os.path.join(idp, 'liquidity.csv'), index_col=0)
        elif model == 'ff5':
            divideMethod = '2x3'  # TODO:other method such as '2x2' and '2x2x2x2' can be chosed for ff5 model.
            iv['rp'] = pd.read_csv(os.path.join(bdp, 'rp.csv'), index_col=0)['rp']
            for factor in ['smb', 'hml', 'rmw', 'cma']:
                iv[factor] = pd.read_csv(os.path.join(factorRetPath, '%s_%s.csv' % (divideMethod, factor)), index_col=0)[
                    factor]
        elif model == 'hxz4':  # Hou,Xue and Zhang (2015a)
            iv['rp'] = pd.read_csv(os.path.join(bdp, 'rp.csv'), index_col=0)['rp']
            iv['smb'] = pd.read_csv(os.path.join(hxz4FactorP, 'rsmb.csv'), index_col=0)
            iv['roe'] = pd.read_csv(os.path.join(hxz4FactorP, 'rroe.csv'), index_col=0)
            iv['ia'] = pd.read_csv(os.path.join(hxz4FactorP, 'ria.csv'), index_col=0)

        iv.to_csv(os.path.join(bmmp,model+'.csv'))

# get_benchmarkModels()


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
        iv=pd.read_csv(os.path.join(bmmp,model+'.csv'),index_col=0)


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
    # iv=pd.DataFrame()
    if model in ['capm','ff3','carhart4','liq4','ff5','hxz4']:
        iv=pd.read_csv(os.path.join(bmmp,model+'.csv'),index_col=0)
    else:
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


#=======================================TODO: construct my model
def getPlayingField():
    tmpdf=pd.read_csv(os.path.join(myFactorPath,'spreadAlphat.csv'),index_col=0)
    tmpdf[tmpdf<2]=np.NaN
    tmpdf=tmpdf.dropna(axis=0,how='all')
    indicators=tmpdf.index.tolist()

    indicators1=[fn[:-4] for fn in os.listdir(fip)]
    indicators2=[fn[:-4] for fn in os.listdir(myIndicatorPath)]

    for indicator in indicators:
        df=''
        if indicator in indicators1:
            df=pd.read_csv(os.path.join(fip,indicator+'.csv'),index_col=0)
        elif indicator in indicators2:
            df=pd.read_csv(os.path.join(myIndicatorPath,indicator+'.csv'),index_col=0)
        df.index = [ind[:-3] for ind in df.index]
        newIndex = [ind for ind in df.index if ind.endswith('12')]
        df = df.reindex(index=newIndex)
        df.to_csv(os.path.join(os.path.join(pfip,indicator+'.csv')))

    size = pd.read_csv(os.path.join(idp, 'size.csv'), index_col=0)
    newIndex = [ind for ind in size.index if ind.endswith('06')]
    size = size.reindex(index=newIndex)
    size.index = [str(int(ind.split('-')[0]) - 1) + '-12' for ind in size.index]
    size.to_csv(os.path.join(pfip,'size.csv'))

    btm = pd.read_csv(os.path.join(idp, 'btm.csv'), index_col=0)
    btm.index = [str(int(ind.split('-')[0]) - 1) + '-12' for ind in btm.index]
    btm.to_csv(os.path.join(pfip,'btm.csv'))


def getPlayingFieldIndicatorId():
    fns=os.listdir(pfip)
    for fn in fns:
        df = pd.read_csv(os.path.join(pfip, fn), index_col=0)
        id2 = getSortedPortId(df, 2)
        id3 = getSortedPortId(df, 3)
        id10 = getSortedPortId(df, 10)

        id2.to_csv(os.path.join(indid2p,fn))
        id3.to_csv(os.path.join(indid3p,fn))
        id10.to_csv(os.path.join(indid10p,fn))
        print fn

#TODO:is the time delay right or not?
#TODO:observe the history lenght of the playing field indicators.

#==================================find new valid model=======================
def buildTestModels():
    cwd=os.getcwd()
    scriptPath=os.path.join(cwd,'multi_buildTestModels.py')
    os.system('python %s'%scriptPath)


# buildTestModels()

def _getValidModels():
    validModels=['capm','ff3','carhart4','liq4','ff5','hxz4']
    fns=os.listdir(mdp)
    for k, fn in enumerate(fns):
        df = pd.read_csv(os.path.join(mdp, fn), index_col=0)
        df = df.dropna(axis=0, how='any')
        if df.shape[0] < 100:
            corr = df.corr()
            np.fill_diagonal(corr.values, 0)
            if corr.abs().max().max() < 0.8:  # delete those collinear model
                validModels.append(fn[:-4])
    return validModels

def getPlayingFieldIndicatorPortRet():
    cwd=os.getcwd()
    scriptPath=os.path.join(cwd,'multi_getPlayingFieldIndicatorPortRet.py')
    os.system('python %s'%scriptPath)



def _reg(df,model):
    if model in ['capm','ff3','carhart4','liq4','ff5','hxz4']:
        slope, t, r2, resid, grs, grsp = regressBenchmark(df, model)
        return slope,t,r2,resid,grs,grsp
    else:
        iv=pd.read_csv(os.path.join(mdp,model+'.csv'),index_col=0)
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
            if df.shape[0] > iv.shape[
                1] + 1:  # make sure that the number of samples is larger than the number of factors plus one.
                coef, t, r2, resid = pandasu.reg(df)
                COEF.loc[col] = coef
                T.loc[col] = t
                R2.loc[col] = r2
                RESID[col] = pd.Series(resid, index=df.index)

        alpha = np.mat(COEF['constant']).T
        factor = iv.as_matrix()
        GRS, GRSp = GRS_test(factor, RESID.as_matrix(), alpha)

        return COEF, T, R2, RESID, GRS, GRSp

def regressAlltestModels():
    grsDf=pd.DataFrame()
    grspDf=pd.DataFrame()

    fns=os.listdir(iprp)

    # filter the model with too short history
    models=_getValidModels()

    for n,fn in enumerate(fns):
        df = pd.read_csv(os.path.join(iprp, fn), index_col=0)
        for c,model in enumerate(models):
            directory=os.path.join(regp,fn[:-4])
            directory = directory.replace(' ', '')#There are some space in fn which is invalid character as file name.
            if not os.path.exists(directory):
                os.makedirs(directory)
            slope,t,r2,resid,grs,grsp=_reg(df,model)

            slope.to_csv(os.path.join(directory,'slope_%s.csv'%model))
            t.to_csv(os.path.join(directory,'t_%s.csv'%model))
            r2.to_csv(os.path.join(directory,'r2_%s.csv'%model))
            resid.to_csv(os.path.join(directory,'resid_%s.csv'%model))

            grsDf.loc[fn[:-4],model]=grs
            grspDf.loc[fn[:-4],model]=grsp
            print n,c
    grsDf.to_csv(os.path.join(pfp,'grs.csv'))
    grspDf.to_csv(os.path.join(pfp,'grsp.csv'))

# regressAlltestModels()


#estimate Alpha and Alphat
def get_alphaAndAlphat():
    models=_getValidModels()
    fns=os.listdir(iprp)

    for n, fn in enumerate(fns):
        ALPHA = pd.DataFrame()
        ALPHAT = pd.DataFrame()
        for k,model in enumerate(models):
            df = pd.read_csv(os.path.join(iprp, fn), index_col=0)
            alpha, alphat = estimateAlpha(df, model)
            ALPHA[model] = alpha.iloc[:, 0]
            ALPHAT[model] = alphat.iloc[:, 0]
            print n,k
        ALPHA.to_csv(os.path.join(alphap, fn))
        ALPHAT.to_csv(os.path.join(alphatp, fn))


fns=os.listdir(alphap)

alpha=pd.DataFrame()
alphat=pd.DataFrame()
for fn in fns:
    df1=pd.read_csv(os.path.join(alphap,fn),index_col=0)
    df2=pd.read_csv(os.path.join(alphatp,fn),index_col=0)
    alpha[fn[:-4]]=df1.loc['10-1']
    alphat[fn[:-4]]=df2.loc['10-1']

alpha=alpha.T
alphat=alphat.T

for col in alphat.columns:
    alphat.loc['gt2',col]=alphat[alphat[col]>2.0].shape[0]
    alphat.loc['lt-2',col]=alphat[alphat[col]<-2.0].shape[0]
    alphat.loc['sum',col]=alphat.loc['gt2',col]+alphat.loc['lt-2',col]

newIndex=['gt2','lt-2','sum']+[ind for ind in alphat.index if ind not in ['gt2','lt-2','sum']]
alphat=alphat.reindex(index=newIndex)

alphat=alphat.sort_values('sum',axis=1)

# alphat=alphat[alphat.loc['sum'].sort_values().index]

alpha.to_csv(os.path.join(pfp,'alpha.csv'))
alphat.to_csv(os.path.join(pfp,'alphat.csv'))

















