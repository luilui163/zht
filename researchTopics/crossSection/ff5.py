#-*-coding: utf-8 -*-
#author:tyhj
#ff5.py 2017/7/31 20:04
import numpy as np
import pandas as pd
import os
import statsmodels.api as sm

from zht.util.dfFilter import filterDf
from zht.researchTopics.crossSection.params import sp,dp
from zht.researchTopics.crossSection.dataAPI import get_df,save_df
from zht.util import mathu
from zht.util import pandasu
from zht.researchTopics.crossSection.plot import get_3dbar,get_3dline
from itertools import combinations
import scipy
from zht.util import statu

def get_factorId(tbname,param):
    '''
    :param tbname:
    :param param:an int number or a list of breakpoints such as [0.3,0.7]
    :return:
    '''
    path = os.path.join(dp, '%sId_%s.csv' % (tbname,param))
    if os.path.exists(path):
        ids=pd.read_csv(path,index_col=0)
        return ids
    else:
        df=get_df(tbname)

        nfc=get_df('nfc')['Stkcd'].values #TODO: important,financial stocks are filtered
        nfc=[str(n) for n in nfc]
        cols=[s for s in df.columns if s in nfc]
        df=df[cols]

        ids=pd.DataFrame(columns=df.columns)
        for month in df.index.tolist():
            sub = df.loc[month].to_frame()
            sub = sub.dropna()
            sub['id'] = mathu.getPortId(sub, param)
            ids.loc[month] = sub['id']
            print month
        ids.to_csv(path)
        return ids

def get_portId(vars,model):
    '''
    :param vars:a list or tuple like ['size','op'] and so on
    :param model:'5x5','2x2','2x3' or '2x2x2x2'
    :return:
    '''
    if not len(vars)==len(model.split('x')):
        raise ValueError('vars do not match the model')
    path = os.path.join(dp, 'portId_%s_%s.csv' % ('_'.join(vars), model))
    if not os.path.exists(path):
        if model=='2x3':
            id1=get_factorId(vars[0],2)
            id2=get_factorId(vars[1],3)
            id1, id2 = pandasu.get_inter_frame([id1,id2])
            portId = id1 * 10 + id2
            portId.to_csv(path)
            return portId
        elif model=='2x2':
            id1=get_factorId(vars[0],2)
            id2=get_factorId(vars[1],2)
            id1, id2 = pandasu.get_inter_frame([id1,id2])
            portId = id1 * 10 + id2
            portId.to_csv(path)
            return portId
        elif model=='5x5':
            id1=get_factorId(vars[0],5)
            id2=get_factorId(vars[1],5)
            id1, id2 = pandasu.get_inter_frame([id1,id2])
            portId = id1 * 10 + id2
            portId.to_csv(path)
            return portId
        elif model=='2x4x4':
            id1=get_factorId(vars[0],2)
            id2=get_factorId(vars[1],4)
            id3=get_factorId(vars[2],4)
            id1,id2,id3=pandasu.get_inter_frame([id1,id2,id3])
            portId=id1*100+id2*10+id3
            portId.to_csv(path)
            return portId
        elif model=='2x2x2x2':
            id1=get_factorId(vars[0],2)
            id2=get_factorId(vars[1],2)
            id3=get_factorId(vars[2],2)
            id4=get_factorId(vars[3],2)
            id1,id2,id3,id4=pandasu.get_inter_frame([id1,id2,id3,id4])
            portId=id1*1000+id2*100+id3*10+id4
            portId.to_csv(path)
            return portId

    else:
        portId=pd.read_csv(path,index_col=0)
        return portId


def get_portRet(vars,model,recal=False):
    '''
    :param vars:a list or tuple like ['size','op'] and so on
    :param model:'5x5','2x2','2x3' or '2x2x2x2'
    :return:
    '''
    if not len(vars)==len(model.split('x')):
        raise ValueError('vars do not match the model')

    path = os.path.join(dp, 'portRet_%s_%s.csv' % ('_'.join(vars), model))
    if os.path.exists(path) and recal==False:
        return pd.read_csv(path,index_col=0)
    else:
        portId=get_portId(vars,model).T
        ret=get_df('ret')
        weight=get_df('weight')

        ports=np.sort([p for p in portId.iloc[:,-1].unique() if not np.isnan(p)])

        portRet=pd.DataFrame()
        for month in portId.columns.tolist():
            year=month[:4]
            validmonths = [year + '-0' + str(i) for i in range(7, 10)]
            validmonths += [year + '-1' + str(i) for i in range(3)]
            validmonths += [str(int(year) + 1) + '-0' + str(i) for i in range(1, 7)]

            for port in ports:
                stocks=portId[portId[month]==port].index.tolist()
                for validmonth in validmonths:
                    if validmonth in ret.index.tolist():
                        try:#There may no intersection stocks between ret columns and stocks,especially at the start of the 1990s
                            tmp=pd.DataFrame()
                            tmp['ret']=ret.loc[validmonth,stocks]
                            tmp['weight']=weight.loc[validmonth,stocks]
                            tmp=tmp.dropna(axis=0,how='any')
                            pr=pandasu.mean_self(tmp,'ret','weight')
                            portRet.loc[validmonth,port]=pr
                        except KeyError:
                            portRet.loc[validmonth,port]=np.NaN
                    else:
                        portRet.loc[validmonth,port]=np.NaN
            print month
        portRet=portRet.dropna(axis=0,how='any')
        save_df(portRet,path[:-4])
        return portRet

def cal_portRet():
    for var in ['btm','op','inv']:
        vars=['size',var]
        get_portRet(vars,'2x2')
        get_portRet(vars,'2x3')
        get_portRet(vars,'5x5')
        print var

    vars=['size','btm','op','inv']
    get_portRet(vars,'2x2x2x2')

    for vars in [['size','btm','op'],['size','btm','inv'],['size','op','inv']]:
        get_portRet(vars,'2x4x4')
        print vars

def get_portEret(vars,model):
    path = os.path.join(dp, 'portEret_%s_%s.csv' % ('_'.join(vars), model))
    portRet=get_portRet(vars,model,recal=False)
    rf=get_df('rf')
    portEret=portRet.sub(rf['rf'],axis=0)
    portEret=portEret.dropna(axis=0,how='any')
    portEret.to_csv(path)
    return portEret

def cal_portErets():
    for var in ['btm', 'op', 'inv']:
        vars = ['size', var]
        get_portEret(vars, '5x5')
        print var
    for vars in [['size', 'btm', 'op'], ['size', 'btm', 'inv'], ['size', 'op', 'inv']]:
        get_portEret(vars, '2x4x4')
        print vars

#ff5 table1
def get_eret_fig():
    n=5
    vars=['size','btm','op','inv']
    combs=combinations(vars,2)
    for (var1,var2) in combs:
        portEret=get_portEret(var1,var2,n)
        # fig=get_3dbar(portEret,var1,var2)
        lineFig=get_3dline(portEret,var1,var2)
        barFig=get_3dbar(portEret,var1,var2)
        barFig.savefig(r'D:\quantDb\researchTopics\crossSection\data\ff5\fig\3dbar\%s_%s.png'%(var1,var2))
        lineFig.savefig(r'D:\quantDb\researchTopics\crossSection\data\ff5\fig\3dline\%s_%s.png'%(var1,var2))


def _get_factor_portRet(validmonth,stocks):
    ret=get_df('ret')
    weight=get_df('weight')
    tmp = pd.DataFrame()
    if validmonth in ret.index.tolist():
        tmp['ret'] = ret.loc[validmonth, stocks]  # TODO: validmonth rathar than month
        tmp['weight'] = weight.loc[validmonth, stocks]
        tmp = tmp.dropna(axis=0, how='any')
        portRet = pandasu.mean_self(tmp, 'ret', 'weight')
        return portRet
    else:
        return np.NaN
#TODO: cal factor return

def get_factorRet_2x3():
    model='2x3'

    vars=['size','btm','op','inv']
    factorName=['smb','hml','rmw','cma']#TODO:notice the sequence of the variables ['size','btm','op','inv']
    dd={a:b for a,b in zip(vars,factorName)}

    for var in ['btm','op','inv']:
        vars=['size',var]
        path1 = os.path.join(dp, 'portId_%s_%s.csv' % ('_'.join(vars), model))
        portId=pd.read_csv(path1,index_col=0).T

        factor = pd.DataFrame(columns=['smb', var])
        months=portId.columns.tolist()
        for month in months:
            year = month[:4]
            validmonths = [year + '-0' + str(i) for i in range(7, 10)]
            validmonths += [year + '-1' + str(i) for i in range(3)]
            validmonths += [str(int(year) + 1) + '-0' + str(i) for i in range(1, 7)]

            aa = portId[portId[month] == 11].index.tolist()
            ab = portId[portId[month] == 12].index.tolist()
            ac = portId[portId[month] == 13].index.tolist()

            ba = portId[portId[month] == 21].index.tolist()
            bb = portId[portId[month] == 22].index.tolist()
            bc = portId[portId[month] == 23].index.tolist()

            for validmonth in validmonths:
                aaret=_get_factor_portRet(validmonth,aa)
                abret=_get_factor_portRet(validmonth,ab)
                acret=_get_factor_portRet(validmonth,ac)

                baret=_get_factor_portRet(validmonth,ba)
                bbret=_get_factor_portRet(validmonth,bb)
                bcret=_get_factor_portRet(validmonth,bc)

                smb=(aaret+abret+acret)/3.0-(baret+bbret+bcret)/3.0
                fr=(acret+bcret)/2.0-(aaret+baret)/2.0

                if var=='inv':
                    fr=-fr

                factor.loc[validmonth]=[smb,fr]
                print validmonth
        factor.to_csv(os.path.join(dp,'factorRet_%s_%s_%s.csv'%(tuple(vars+[model]))))
        print vars


    smb=pd.DataFrame()
    for var in ['btm','op','inv']:
        vars=['size',var]
        path=os.path.join(dp,'factorRet_%s_%s_%s.csv'%(tuple(vars+[model])))
        sub=pd.read_csv(path,index_col=0)
        smb[var]=sub['smb']

        sub=sub[[var]]
        sub.columns = [dd[var]]
        sub.to_csv(os.path.join(dp,'ff5_factorRet_%s_%s.csv'%(dd[var],model)))

    smb=smb.mean(axis=1).to_frame()
    smb.columns=['smb']
    smb.to_csv(os.path.join(dp,'ff5_factorRet_smb_%s.csv'%model))

def get_factorRet_2x2():
    model = '2x2'

    vars=['size','btm','op','inv']
    factorName=['smb','hml','rmw','cma']#TODO:notice the sequence of the variables ['size','btm','op','inv']
    dd={a:b for a,b in zip(vars,factorName)}

    for var in ['btm', 'op', 'inv']:
        vars = ['size', var]
        path1 = os.path.join(dp, 'portId_%s_%s.csv' % ('_'.join(vars), model))
        portId = pd.read_csv(path1, index_col=0).T

        factor = pd.DataFrame(columns=['smb', var])
        months = portId.columns.tolist()
        for month in months:
            year = month[:4]
            validmonths = [year + '-0' + str(i) for i in range(7, 10)]
            validmonths += [year + '-1' + str(i) for i in range(3)]
            validmonths += [str(int(year) + 1) + '-0' + str(i) for i in range(1, 7)]

            aa = portId[portId[month] == 11].index.tolist()
            ab = portId[portId[month] == 12].index.tolist()

            ba = portId[portId[month] == 21].index.tolist()
            bb = portId[portId[month] == 22].index.tolist()

            for validmonth in validmonths:
                aaret = _get_factor_portRet(validmonth, aa)
                abret = _get_factor_portRet(validmonth, ab)

                baret = _get_factor_portRet(validmonth, ba)
                bbret = _get_factor_portRet(validmonth, bb)

                smb = (aaret + abret) / 2.0 - (baret + bbret) / 2.0
                fr = (abret + bbret) / 2.0 - (aaret + baret) / 2.0
                if var=='inv':
                    fr=-fr

                factor.loc[validmonth] = [smb, fr]
                print validmonth
        factor.to_csv(os.path.join(dp, 'factorRet_%s_%s_%s.csv' % (tuple(vars + [model]))))
        print vars

    smb = pd.DataFrame()
    for var in ['btm', 'op', 'inv']:
        vars = ['size', var]
        path = os.path.join(dp, 'factorRet_%s_%s_%s.csv' % (tuple(vars + [model])))
        sub = pd.read_csv(path, index_col=0)
        smb[var] = sub['smb']

        sub = sub[[var]]
        sub.columns=[dd[var]]
        sub.to_csv(os.path.join(dp, 'ff5_factorRet_%s_%s.csv' % (dd[var],model)))

    smb = smb.mean(axis=1).to_frame()
    smb.columns = ['smb']
    smb.to_csv(os.path.join(dp, 'ff5_factorRet_smb_%s.csv'%model))

def get_factorRet_2x2x2x2():
    model = '2x2x2x2'
    vars=['size','btm','op','inv']
    factorName=['smb','hml','rmw','cma']#TODO:notice the sequence of the variables ['size','btm','op','inv']
    dd={a:b for a,b in zip(vars,factorName)}
    path1=os.path.join(dp, 'portId_%s_%s.csv' % ('_'.join(vars), model))
    portId = pd.read_csv(path1, index_col=0).T


    factor = pd.DataFrame(columns=['smb', 'hml','rmw','cma'])

    months = portId.columns.tolist()
    for month in months:#TODO: all
        year = month[:4]
        validmonths = [year + '-0' + str(i) for i in range(7, 10)]
        validmonths += [year + '-1' + str(i) for i in range(3)]
        validmonths += [str(int(year) + 1) + '-0' + str(i) for i in range(1, 7)]

        portId=portId.fillna(0)
        portId=portId.astype(int)
        ports=np.unique(portId)
        ports=sorted([p for p in ports if p!=0])

        for validmonth in validmonths:
            for var in vars:
                ind=vars.index(var)
                subport1=[p for p in ports if str(p)[ind]=='1']
                subport2=[p for p in ports if str(p)[ind]=='2']

                rets1=[]
                for subport in subport1:
                    stocks=portId[portId[month]==subport].index.tolist()
                    ret=_get_factor_portRet(validmonth,stocks)
                    rets1.append(ret)

                rets2=[]
                for subport in subport2:
                    stocks=portId[portId[month]==subport].index.tolist()
                    ret=_get_factor_portRet(validmonth,stocks)
                    rets2.append(ret)
                if var in ['size','inv']:
                    factorRet=np.mean(rets1)-np.mean(rets2)
                else:
                    factorRet=np.mean(rets2)-np.mean(rets1)
                factor.loc[validmonth,dd[var]]=factorRet
                print validmonth,var
    for _,value in dd.iteritems():
        tmp=factor[value].to_frame()
        tmp.columns=[value]
        tmp.to_csv(os.path.join(dp, 'ff5_factorRet_%s_%s.csv'%(value,model)))

#TODO:validate the factor return
def validate_ff5_factorRet():
    tbname='STK_MKT_FivefacMonth'
    df=pd.read_csv(os.path.join(sp,tbname+'.csv'))
    q='MarkettypeID == P9709'
    df=filterDf(df,q)
    df=df.set_index('TradingMonth')

    typeDict={1:'2x3',2:'2x2',3:'2x2x2x2'}

    for k,v in typeDict.iteritems():
        smb=df[df['Portfolios']==k]['SMB1'].to_frame()
        smb['mysmb']=pd.read_csv(os.path.join(dp,'ff5_factorRet_smb_%s.csv'%v),index_col=0)['smb']

        hml=df[df['Portfolios']==k]['HML1'].to_frame()
        hml['myhml']=pd.read_csv(os.path.join(dp,'ff5_factorRet_hml_%s.csv'%v),index_col=0)['hml']

        rmw=df[df['Portfolios']==k]['RMW1'].to_frame()
        rmw['myrmw']=pd.read_csv(os.path.join(dp,'ff5_factorRet_rmw_%s.csv'%v),index_col=0)['rmw']

        cma=df[df['Portfolios']==k]['CMA1'].to_frame()
        cma['mycma']=pd.read_csv(os.path.join(dp,'ff5_factorRet_cma_%s.csv'%v),index_col=0)['cma']

        rp=df[df['Portfolios']==k]['RiskPremium1'].to_frame()
        rp['myrp']=get_df('rp')['rp']

        smb.dropna(axis=0).cumsum().plot().get_figure().savefig(r'D:\quantDb\researchTopics\crossSection\data\ff5\fig\validate_ff5\%s\smb.png'%v)
        hml.dropna(axis=0).cumsum().plot().get_figure().savefig(r'D:\quantDb\researchTopics\crossSection\data\ff5\fig\validate_ff5\%s\hml.png'%v)
        rmw.dropna(axis=0).cumsum().plot().get_figure().savefig(r'D:\quantDb\researchTopics\crossSection\data\ff5\fig\validate_ff5\%s\rmw.png'%v)
        cma.dropna(axis=0).cumsum().plot().get_figure().savefig(r'D:\quantDb\researchTopics\crossSection\data\ff5\fig\validate_ff5\%s\cma.png'%v)
        rp.dropna(axis=0).cumsum().plot().get_figure().savefig(r'D:\quantDb\researchTopics\crossSection\data\ff5\fig\validate_ff5\%s\rp.png'%v)

def regress():
    directory=r'D:\quantDb\researchTopics\crossSection\data\ff5\regress'
    factors=['smb','hml','rmw','cma']
    for model in ['2x2','2x3','2x2x2x2']:
        for vars in [['size','btm'],['size','inv'],['size','op']]:
            path=os.path.join(dp,'portEret_%s_5x5.csv'%('_'.join(vars)))
            dv=pd.read_csv(path,index_col=0)
            iv=pd.DataFrame()
            for factor in factors:
                iv[factor]=pd.read_csv(os.path.join(dp,'ff5_factorRet_%s_%s.csv'%(factor,model)),index_col=0)[factor]
            iv['rp']=pd.read_csv(os.path.join(dp,'rp.csv'),index_col=0)['rp']


            slopes=pd.DataFrame(columns=['constant']+iv.columns.tolist())
            ts=pd.DataFrame(columns=['constant']+iv.columns.tolist())
            r2s=pd.DataFrame(columns=['r2'])
            resids=pd.DataFrame()

            for col in dv.columns.tolist():
                df = pd.DataFrame()
                df[col]=dv[col]
                df[iv.columns.tolist()]=iv #TODO: or iv[iv.columns]
                df=df.dropna(axis=0,how='any')
                if df.shape[0]>iv.shape[1]+1:#make sure that the number of samples is larger than the number of factors plus one.
                    slope,t,r2,resid=pandasu.reg(df)
                    slopes.loc[col]=slope
                    ts.loc[col]=t
                    r2s.loc[col]=r2
                    resids[col]=pd.Series(resid,index=df.index)

            slopes.to_csv(os.path.join(directory,'%s_%s_slope.csv'%(model,'_'.join(vars))))
            ts.to_csv(os.path.join(directory,'%s_%s_t.csv'%(model,'_'.join(vars))))
            r2s.to_csv(os.path.join(directory,'%s_%s_r2.csv'%(model,'_'.join(vars))))
            resids.to_csv(os.path.join(directory,'%s_%s_resid.csv'%(model,'_'.join(vars))))
            print model,vars

def get_GRS():
    for vars in [['size','btm'],['size','inv'],['size','op']]:
        for model in ['2x2','2x3','2x2x2x2']:
            # matlab method
            factors = ['smb', 'hml', 'rmw', 'cma']
            iv = pd.DataFrame()
            for factor in factors:
                iv[factor] = pd.read_csv(os.path.join(dp, 'ff5_factorRet_%s_%s.csv' % (factor, model)), index_col=0)[factor]
            iv['rp'] = pd.read_csv(os.path.join(dp, 'rp.csv'), index_col=0)['rp']
            # TxL Matrix of Excess factor returns
            iv = iv.dropna(axis=0, how='any').as_matrix()

            resid = pd.read_csv(r'D:\quantDb\researchTopics\crossSection\data\ff5\regress\%s_%s_resid.csv' % (model, '_'.join(vars)), index_col=0)
            # TxN Matrix of residuals from TS-regression
            resid=resid.as_matrix()

            alpha = pd.read_csv(r'D:\quantDb\researchTopics\crossSection\data\ff5\regress\%s_%s_slope.csv' % (model, '_'.join(vars)),index_col=0).iloc[:, 0].values
            # Nx1 Vector of intercepts from TS-regression
            alpha = np.mat(alpha).T

            GRS,pvalue=statu.GRS_test(iv,resid,alpha)
            print vars,model,GRS,pvalue





#TODO: 标准化ff3和ff5，以及GRS，

#TODO:找出影响股票收益的因子。fama-macbeth?

#TODO:delete the stocks listed less than two years
#TODO:financial stocks or not ?
#TODO:架构，类，

#TODO:build a package for this subject like https://cran.r-project.org/web/packages/GRS.test/GRS.test.pdf


#TODO: get new factors

#TODO:the month of the factors are the date in which to construct portfolios





