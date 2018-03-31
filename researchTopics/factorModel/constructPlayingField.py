#-*-coding: utf-8 -*-
#author:tyhj
#constructPlayingField.py 2017/9/20 23:54

'''
choose those factors that have a significant effect on return
'''
import pandas as pd



from zht.util.quantu import plotCumulativeRet,informationRatio
from params import *
from tools import *

#=================method 1:high port minus low port=========================
def plotSpread():
    fns=os.listdir(idrp)
    for fn in fns:
        portRet=pd.read_csv(os.path.join(idrp,fn),index_col=0)
        spread=portRet.iloc[:,-1]-portRet.iloc[:,0]

        fig=plotCumulativeRet(spread)
        fig.savefig(os.path.join(spfp,fn[:-4]+'.png'))

def getIR():
    fns=os.listdir(idrp)
    irdf=pd.DataFrame()
    for fn in fns:
        df=pd.read_csv(os.path.join(idrp,fn),index_col=0)
        spread=df.iloc[:,-1]-df.iloc[:,0]
        ir=informationRatio(spread)
        irdf.loc[fn[:-4],'ir']=ir
        print fn
    irdf['abs_ir']=irdf['ir'].abs()
    irdf=irdf.sort_values('abs_ir',ascending=False)
    irdf.to_csv(os.path.join(cpfp,'spreadIR.csv'))


def regressAllIndicatorsOnBenchMarkModels():
    grsDf=pd.DataFrame()
    grspDf=pd.DataFrame()
    fns=os.listdir(idrp)
    for n,fn in enumerate(fns):
        for model in ['capm','ff3','carhart4','liq4','ff5','hxz4']:
            df=pd.read_csv(os.path.join(idrp,fn),index_col=0)
            directory=os.path.join(regp,fn[:-4])
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
    grsDf.to_csv(os.path.join(cpfp,'grs.csv'))
    grspDf.to_csv(os.path.join(cpfp,'grsp.csv'))



#========================find the mispricing factors======================
#method 1:method as table 4 in (Pástor and Stambaugh 2003)
def calAlphaAndAlphat():
    fns=os.listdir(idrp)
    for n, fn in enumerate(fns):
        ALPHA=pd.DataFrame()
        ALPHAT=pd.DataFrame()
        for model in ['capm', 'ff3', 'carhart4', 'liq4', 'ff5','hxz4']:
            df = pd.read_csv(os.path.join(idrp, fn), index_col=0)
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
    spreadAlphat.to_csv(os.path.join(cpfp,'spreadAlphat.csv'))

def analyseR2():
    factornames= os.listdir(regp)
    avgR2=pd.DataFrame()
    for factorname in factornames:
        fns=os.listdir(os.path.join(regp,factorname))
        fns=[fn for fn in fns if fn.startswith('r2')]

        for fn in fns:
            avgR2.loc[factorname,fn.split('_')[-1][:-4]]=pd.read_csv(os.path.join(regp, factorname,fn), index_col=0)['r2'].mean()
        print factorname

    avgR2.to_csv(os.path.join(cpfp,'avgR2.csv'))


def getValidIndicators():
    '''
    get those indicators which can not be explained
    by the classical models.These indicators can be used to
    build test models.

    :return:list

    '''
    df=pd.read_csv(os.path.join(cpfp,'spreadAlphat.csv'),index_col=0)
    # df=df.sort_values('ff3_abs',ascending=False)
    # df.loc['lg2']=[df[df[col]>2].shape[0] for col in df.columns]
    # newIndOrder=['lg2']+[ind for ind in df.index if ind !='lg2']
    # df=df.reindex(index=newIndOrder)
    #
    #
    # df.to_csv(os.path.join(cpfp,'spreadAlphat_analysis.csv'))

    # validIndicators=['size','btm','inv','op']
    #
    # absCols=[col for col in df.columns if col.endswith('abs')]
    # for col in absCols:
    #     indicators=df[df[col]>2].index.tolist()
    #     for ind in indicators:
    #         if ind not in validIndicators:
    #             validIndicators.append(ind)
    #len(validIndicators)=222

    validIndicators=['size','btm','inv','op']
    #TODO:some indicators may be equal even though their name are different.
    for ind in df[df['ff3']>2].index:
        if ind not in validIndicators:
            validIndicators.append(ind)

    return validIndicators





def do():
    regOnAllPossiblemodels()






#TODO:method 2:fama mecbeth

#TODO:analyse the meaning of the factors in Mipricing factor model.
#TODO:find new possible factors from resset and wind
#TODO:analyse whether the time-lag is right or not



#TODO:refer to regressionModels.py in assetPricing to add the other functions
#=======================================












#TODO:factors correlation



if __name__=='__main__':
    pass
    #TODO:






