#-*-coding: utf-8 -*-
#author:tyhj
#ff3.py 2017/7/31 16:05
import numpy as np
import pandas as pd
import os
import statsmodels.api as sm

from zht.util.dfFilter import filterDf
from zht.researchTopics.crossSection.params import sp
from zht.researchTopics.crossSection.dataAPI import get_df,save_df
from zht.util import mathu
from zht.util import pandasu
from itertools import combinations

def _regress(eret,smb,hml,rp,path):
    '''
    :param eret: dataframe
    :param smb: series
    :param hml: series
    :param rp: series
    :param path: diractory
    '''
    coef = pd.DataFrame(columns=['const', 'smb', 'hml', 'rp'])
    t = pd.DataFrame(columns=['const', 'smb', 'hml', 'rp'])
    r2 = pd.Series()
    errorDfs = []

    for groupId in eret.columns:
        tmpdf = pd.DataFrame()
        tmpdf['eret'] = eret[groupId]
        tmpdf['smb'] = smb
        tmpdf['hml'] = hml
        tmpdf['rp'] = rp
        tmpdf = tmpdf.dropna(axis=0, how='any')

        X = tmpdf[['smb', 'hml', 'rp']].as_matrix()
        X = sm.add_constant(X)
        y = tmpdf['eret'].values

        model = sm.OLS(y, X)
        results = model.fit()

        coef.loc[groupId] = results.params
        t.loc[groupId] = results.tvalues
        r2[groupId] = results.rsquared_adj

        err = pd.DataFrame(results.resid, index=tmpdf.index, columns=[groupId])
        errorDfs.append(err)

    errorDf = pd.concat(errorDfs, axis=1)

    coef.loc['mean']=coef.mean()
    r2.loc['mean']=r2.mean()
    t.loc['mean']=t.mean()


    coef.to_csv(os.path.join(path,'coef.csv'))
    t.to_csv(os.path.join(path,'t.csv'))
    r2.to_csv(os.path.join(path,'r2.csv'))
    errorDf.to_csv(os.path.join(path,'errorDf.csv'))

#regress on my data
def regress_mydata():
    eret=get_df('portEret')
    rp=get_df('rp')
    factor=get_df('smb_hml')

    rp=rp['rp']
    smb=factor['smb']
    hml=factor['hml']
    path=r'D:\quantDb\researchTopics\crossSection\data\regressOnMyData'
    _regress(eret,smb,hml,rp,path)

#regress on resset
def regress_resset():
    eret=get_df('portEret')
    factor = pd.read_csv(r'D:\quantDb\resset\THRFACDAT_MONTHLY.csv', index_col=0)
    q1 = 'Exchflg == 0'
    q2 = 'Mktflg == A'
    factor = filterDf(factor, [q1, q2])
    factor = factor.set_index('Date')
    factor.index = [ind[:-3] for ind in factor.index]

    smb1=factor['Smb_tmv']
    hml1=factor['Hml_tmv']
    rp1=factor['Rmrf_tmv']
    path1=r'D:\quantDb\researchTopics\crossSection\data\regressOnRessetData\tmv'

    smb2=factor['Smb_mc']
    hml2=factor['Hml_mc']
    rp2=factor['Rmrf_mc']
    path2=r'D:\quantDb\researchTopics\crossSection\data\regressOnRessetData\mc'

    _regress(eret,smb1,hml1,rp1,path1)
    _regress(eret,smb2,hml2,rp2,path2)

#regress on gta data
def regress_gta():
    eret=get_df('portEret')
    factor=pd.read_csv(r'D:\quantDb\sourceData\gta\data\csv\STK_MKT_ThrfacMonth.csv')
    q='MarkettypeID == P9709'
    factor=filterDf(factor,q)
    factor=factor.set_index('TradingMonth')

    smb1=factor['SMB1']
    hml1=factor['HML1']
    rp1=factor['RiskPremium1']
    path1=r'D:\quantDb\researchTopics\crossSection\data\regressOnGTA\tmv'

    smb2=factor['SMB2']
    hml2=factor['HML2']
    rp2=factor['RiskPremium2']
    path2=r'D:\quantDb\researchTopics\crossSection\data\regressOnGTA\mc'

    _regress(eret,smb1,hml1,rp1,path1)
    _regress(eret,smb2,hml2,rp2,path2)

def regress_using_resset_portRet():
    eret = get_df('portEret_rs_tmv')
    rp = get_df('rp')
    factor = get_df('smb_hml')

    rp = rp['rp']
    smb = factor['smb']
    hml = factor['hml']
    path = r'D:\quantDb\researchTopics\crossSection\data\ressetRegress\mydata'
    _regress(eret, smb, hml, rp, path)

    #--------------------------------
    eret = get_df('portEret_rs_tmv')
    factor = pd.read_csv(r'D:\quantDb\resset\THRFACDAT_MONTHLY.csv', index_col=0)
    q1 = 'Exchflg == 0'
    q2 = 'Mktflg == A'
    factor = filterDf(factor, [q1, q2])
    factor = factor.set_index('Date')
    factor.index = [ind[:-3] for ind in factor.index]

    smb1 = factor['Smb_tmv']
    hml1 = factor['Hml_tmv']
    rp1 = factor['Rmrf_tmv']
    path1 = r'D:\quantDb\researchTopics\crossSection\data\ressetRegress\resset\tmv'

    smb2 = factor['Smb_mc']
    hml2 = factor['Hml_mc']
    rp2 = factor['Rmrf_mc']
    path2 = r'D:\quantDb\researchTopics\crossSection\data\ressetRegress\resset\mc'

    _regress(eret, smb1, hml1, rp1, path1)
    _regress(eret, smb2, hml2, rp2, path2)

    #------------------------------------------------
    eret = get_df('portEret_rs_tmv')
    factor = pd.read_csv(r'D:\quantDb\sourceData\gta\data\csv\STK_MKT_ThrfacMonth.csv')
    q = 'MarkettypeID == P9709'
    factor = filterDf(factor, q)
    factor = factor.set_index('TradingMonth')

    smb1 = factor['SMB1']
    hml1 = factor['HML1']
    rp1 = factor['RiskPremium1']
    path1 = r'D:\quantDb\researchTopics\crossSection\data\ressetRegress\gta\tmv'

    smb2 = factor['SMB2']
    hml2 = factor['HML2']
    rp2 = factor['RiskPremium2']
    path2 = r'D:\quantDb\researchTopics\crossSection\data\ressetRegress\gta\mc'

    _regress(eret, smb1, hml1, rp1, path1)
    _regress(eret, smb2, hml2, rp2, path2)

#======================================================
def regress_comb():
    rp = get_df('rp')
    factor = get_df('smb_hml')

    rp = rp['rp']
    smb = factor['smb']
    hml = factor['hml']
    eret = get_df('portEret')

    dic={'rp':rp,'smb':smb,'hml':hml}

    def reg(vars):
        path=r'D:\quantDb\researchTopics\crossSection\data\regressResult\%s_%s'%(len(vars),'_'.join(vars))
        if not os.path.exists(path):
            os.makedirs(path)

        coef=pd.DataFrame(columns=['const']+vars)
        t=pd.DataFrame(columns=['const']+vars)
        r2=pd.DataFrame(columns=['r2'])
        errorDfs=[]
        for groupId in eret.columns:
            tmpdf=pd.DataFrame()
            tmpdf['eret'] = eret[groupId]
            for var in vars:
                tmpdf[var]=dic[var]
            tmpdf=tmpdf.dropna(axis=0,how='any')
            X=tmpdf[vars].as_matrix()
            X=sm.add_constant(X)
            y=tmpdf['eret'].values

            model = sm.OLS(y, X)
            results = model.fit()

            coef.loc[groupId] = results.params
            t.loc[groupId] = results.tvalues
            r2.loc[groupId,'r2'] = results.rsquared_adj

            err = pd.DataFrame(results.resid, index=tmpdf.index, columns=[groupId])
            errorDfs.append(err)

        errorDf = pd.concat(errorDfs, axis=1)

        coef.loc['mean']=coef.mean()
        r2.loc['mean']=r2.mean()
        t.loc['mean']=t.mean()


        coef.to_csv(os.path.join(path, 'coef.csv'))
        t.to_csv(os.path.join(path, 't.csv'))
        r2.to_csv(os.path.join(path, 'r2.csv'))
        errorDf.to_csv(os.path.join(path, 'errorDf.csv'))

    vars=['rp','smb','hml']
    for i in range(1,4):
        comb=combinations(vars,i)
        for subset in comb:
            reg(list(subset))
            print i,subset

def summary():
    path=r'D:\quantDb\researchTopics\crossSection\data\regressResult'

    dirs=os.listdir(path)
    r2s=pd.DataFrame()
    for d in dirs:
        r2=pd.read_csv(os.path.join(path,d,'r2.csv'),index_col=0)
        r2s[d]=r2['r2']

    print r2s.head()

    r2s.to_csv(os.path.join(path,'r2s.csv'))

#TODO: construct factors and then regress them.






