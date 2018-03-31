#-*-coding: utf-8 -*-
#author:tyhj
#detectFactors.py 2017/9/3 9:13

import pandas as pd
import os
import numpy as np

from zht.util import pandasu
from zht.util import mathu
from zht.data.gta import gtaApi
from zht.util.dfFilter import filterDf
from zht.util.pandasu import flatten2panel
from zht.util.listu import chunkify
from zht.util.quantu import plotCumulativeRet,informationRatio


from params import *
from regressionModels import *


#=================================get raw indicators==================================

def getIndicators():
    '''
    get indicators from the series of '财务指标系列'
    :return:
    '''
    ns=['1','3','8','7','11','4','9','6','5']
    #10,2 are special,there is no colname 'Typrep'
    tbnames=['FI_T'+n for n in ns]
    for tbname in tbnames:
        q='Typrep == A'#combined balance sheet
        df=gtaApi.readFromSrc(tbname)
        df=filterDf(df,q)

        variables=[col for col in df.columns if col not in ['Stkcd','Indcd','Accper','Typrep']]
        tmpdf=pd.read_csv(os.path.join(r'D:\quantDb\sourceData\gta\data\tablesNew',tbname+'.csv'),index_col=0)
        adict={tmpdf['Fldname'].values[i]:tmpdf['Title'].values[i] for i in range(tmpdf.shape[0])}
        for variable in variables:
            indvar='Accper'
            colvar='Stkcd'
            vname=variable
            mydf=flatten2panel(df,indvar,colvar,vname)
            mydf.to_csv(os.path.join(myIndicatorPath,adict[vname]+'.csv'))
            print tbname,vname

def get_financialIndicators():
    tbnames=['FS_Comins','FS_Comscfi','FS_Comscfd','FS_Combas']
    for tbname in tbnames:
        q='Typrep == A'

        namedf=pd.read_csv(os.path.join(r'D:\quantDb\sourceData\gta\data\tablesNew',tbname+'.csv'),index_col=0)
        namedict={namedf['Fldname'].values[i]:namedf['Title'].values[i] for i in range(namedf.shape[0])}

        unvar=['Accper','Stkcd','Typrep']
        indvar='Accper'
        colvar='Stkcd'

        df=gtaApi.readFromSrc(tbname)
        df=filterDf(df,q)
        for vname in df.columns:
            if vname not in unvar:
                indicator=flatten2panel(df,indvar,colvar,vname)
                indicator.to_csv(os.path.join(fip,namedict[vname]+'.csv'))
            print tbname,vname

def getFinancialIndicatorId():
    cwd = os.getcwd()
    scriptPath = os.path.join(cwd, 'multi_getFinancialIndicatorId.py')
    os.system('python %s' % scriptPath)

# getFinancialIndicatorId()

def getFinancialPortRet():
    cwd=os.getcwd()
    scriptPath=os.path.join(cwd,'multi_getFinancialPortRet.py')
    os.system('python %s'%scriptPath)

# getFinancialPortRet()


# tbname='STK_MKT_ValuationMetrics'
# tbname='STK_MKT_StyleBox'
#
# df=gtaApi.readFromSrc(tbname)
# print df.head()





def getIndicatorId():
    cwd=os.getcwd()
    scriptPath=os.path.join(cwd,'multi_getIndicatorId.py')
    os.system('python %s'%scriptPath)

#getIndicatorId()


def getPortRet():
    cwd=os.getcwd()
    scriptPath=os.path.join(cwd,'multi_getPortRet.py')
    os.system('python %s'%scriptPath)

# getPortRet()
def getPortEret():
    rf=pd.read_csv(os.path.join(bdp,'rf.csv'),index_col=0)
    fns=os.listdir(prp)
    for fn in fns:
        portRet=pd.read_csv(os.path.join(prp,fn),index_col=0)
        portEret=portRet.sub(rf['rf'],axis=0)
        portEret=portEret.dropna(axis=0,how='any')
        portEret.to_csv(os.path.join(perp,fn))
        print fn

# getPortEret()

#===========================validate the factors===========================

#method 1:high-low

def highMinusLow(fn):
    df=pd.read_csv(os.path.join(prp,fn),index_col=0)
    spread=df.iloc[:,-1]-df.iloc[:,0]

    fig=plotCumulativeRet(spread)
    fig.savefig(os.path.join(spreadPath,fn[:-4]+'.png'))

def plotSpread():
    fns=os.listdir(prp)
    for fn in fns:
        highMinusLow(fn)
        print fn

def getIR():
    fns=os.listdir(prp)
    irdf=pd.DataFrame()
    for fn in fns:
        df=pd.read_csv(os.path.join(prp,fn),index_col=0)
        spread=df.iloc[:,-1]-df.iloc[:,0]
        ir=informationRatio(spread)
        irdf.loc[fn[:-4],'ir']=ir
        print fn
    irdf['abs_ir']=irdf['ir'].abs()
    irdf=irdf.sort_values('abs_ir',ascending=False)
    irdf.to_csv(os.path.join(myFactorPath,'IR.csv'))

# getIR()


#TODO:method 2:fama mecbeth
#+====================================================================
#regress my factors
def regressAllModels():
    grsDf=pd.DataFrame()
    grspDf=pd.DataFrame()
    fns=os.listdir(prp)
    for n,fn in enumerate(fns):
        for model in ['capm','ff3','carhart4','liq4','ff5','hxz4']:
            df=pd.read_csv(os.path.join(prp,fn),index_col=0)
            directory=os.path.join(regressResultPath,fn[:-4])
            directory = directory.replace(' ', '')#There are some space in fn which is invalid character as file name.
            if not os.path.exists(directory):
                os.makedirs(directory)
            slope,t,r2,resid,grs,grsp=regressBenchmark(df,model)

            slope.to_csv(os.path.join(directory,'slope_%s.csv'%model))
            t.to_csv(os.path.join(directory,'t_%s.csv'%model))
            r2.to_csv(os.path.join(directory,'r2_%s.csv'%model))
            resid.to_csv(os.path.join(directory,'resid_%s.csv'%model))

            grsDf.loc[fn[:-4],model]=grs
            grspDf.loc[fn[:-4],model]=grsp
        print n,fn

    grspDf=grspDf.sort_values('ff3')
    grsDf.to_csv(os.path.join(myFactorPath,'grs.csv'))
    grspDf.to_csv(os.path.join(myFactorPath,'grsp.csv'))


#========================find the mispricing factors======================
#method 1:method as table 4 in (Pástor and Stambaugh 2003)
def analyseAlpha():
    fns=os.listdir(prp)
    for n, fn in enumerate(fns):
        ALPHA=pd.DataFrame()
        ALPHAT=pd.DataFrame()
        for model in ['capm', 'ff3', 'carhart4', 'liq4', 'ff5','hxz4']:
            df = pd.read_csv(os.path.join(prp, fn), index_col=0)
            alpha,alphat=estimateAlpha(df,model)
            ALPHA[model]=alpha.iloc[:,0]
            ALPHAT[model]=alphat.iloc[:,0]
        ALPHA.to_csv(os.path.join(eap,fn))
        ALPHAT.to_csv(os.path.join(eatp,fn))
        print n


def analyseAlphat():
    fns=os.listdir(eatp)
    spreadAlphat=pd.DataFrame()
    for fn in fns:
        df=pd.read_csv(os.path.join(eatp,fn),index_col=0)
        spreadAlphat[fn[:-4]]=df.iloc[-1,:]

    spreadAlphat=spreadAlphat.T

    for col in spreadAlphat.columns:
        spreadAlphat[col+'_abs']=spreadAlphat[col].abs()
    spreadAlphat=spreadAlphat.sort_values('capm_abs')
    spreadAlphat.to_csv(os.path.join(myFactorPath,'spreadAlphat.csv'))

def analyseR2():
    factornames= os.listdir(regressResultPath)
    avgR2=pd.DataFrame()
    for factorname in factornames:
        fns=os.listdir(os.path.join(regressResultPath,factorname))
        fns=[fn for fn in fns if fn.startswith('r2')]

        for fn in fns:
            avgR2.loc[factorname,fn.split('_')[-1][:-4]]=pd.read_csv(os.path.join(regressResultPath, factorname,fn), index_col=0)['r2'].mean()
        print factorname

    avgR2.to_csv(os.path.join(myFactorPath,'avgR2.csv'))


#TODO:analyse the meaning of the factors in Mipricing factor model.
#TODO:find new possible factors from resset and wind
#TODO:analyse whether the time-lag is right or not










