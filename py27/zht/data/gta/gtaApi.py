#-*-coding: utf-8 -*-
#@author:tyhj
import os
import pandas as pd
import numpy as np
from zht.util.stru import cleanStockId
from zht.util.dfFilter import filterDf
from zht.util import pandasu
from zht.util import mathu
from zht.data.resset.ressetApi import getFama3
from zht.data.resset import ressetApi
from zht.util.stru import extractDate


from zht.util.pandasu import flatten2panel
from zht.data.gta.config import processedPath

from zht.data.gta import gtaSettings
import statsmodels.api as sm

def getMkt():
    df=pd.read_csv(r'D:\quantDb\mkt\monthly\mkt.csv',index_col=0)
    df['Stkcd']=cleanStockId(df['Stkcd'])
    df=filterDf(df, gtaSettings.queryMarketType)
    return df

def getIndicator():
    df=pd.read_csv(u'D:\quantDb\每股指标\gta\FI_T9.csv',index_col=0,dtype={'Stkcd':str})
    df['Stkcd'] = cleanStockId(df['Stkcd'])
    df=filterDf(df, gtaSettings.queryReportType)
    return df

def getFama3():
    path=u'D:\quantDb\三因子月\STK_MKT_ThrfacMonth.csv'
    df=pd.read_csv(path,index_col=0)
    df=filterDf(df,gtaSettings.queryFamaMarketType)
    return df

# def getRf():
#     rf=pd.read_csv(r'D:\quantDb\mkt\dataset\rf.csv', index_col=0)
#     return rf

def getRm(recal=False):
    path=r'D:\quantDb\mkt\dataset\rm.csv'
    if recal or not os.path.exists(path):
        mkt=getMkt()
        months = mkt['Trdmnt'].unique().tolist()
        months = sorted(months)[1:]  # 第一个月缺失数据
        rm = pd.DataFrame(columns=['rm'])
        for i in range(1,len(months))[30:]:
            mvdf=mkt[mkt['Trdmnt']==months[i-1]] #TODO: important!!!!!!  use tradable market value of the last month
            mvdf=mvdf.set_index('Stkcd')
            mvdf=mvdf[[gtaSettings.mvType]]
            mvdf.columns=['mv']

            retdf=mkt[mkt['Trdmnt']==months[i]]
            retdf=retdf.set_index('Stkcd')
            retdf=retdf[[gtaSettings.retType]]
            retdf.columns=['ret']

            tmp=pd.concat([mvdf,retdf],axis=1)
            tmp = tmp.dropna(axis=0, how='any')
            if tmp.shape[0]>0:
                r = pandasu.mean_self(tmp, 'ret', 'mv')
                print months[i], r
                rm.loc[months[i], 'rm'] = r
        rm.to_csv(path)
        return rm
    else:
        rm=pd.read_csv(path,index_col=0)
        return rm

#sort size in the june of every year
def getSizeId(sizeNum,recal=False):
    path=r'D:\quantDb\researchTopics\fama\sizeId_%s.csv'%sizeNum
    if recal or not os.path.exists(path):
        mkt=getMkt()
        query='Trdmnt endswith 06'
        dfSize=filterDf(mkt,query)[['Stkcd','Trdmnt',gtaSettings.mvType]]
        junes=sorted(dfSize['Trdmnt'].unique().tolist())

        subdfs=[]
        for june in junes:
            subdf=dfSize[dfSize['Trdmnt']==june]#TODO:how to handle np.NaN?
            # subdf.loc[:,'rank']=subdf[mvType].rank()
            subdf.loc[:,'sizeId']=mathu.getPortId(subdf[gtaSettings.mvType],sizeNum)
            subdf=subdf.set_index('Stkcd')
            del subdf.index.name
            subdf=subdf[['sizeId']]
            subdf.columns=[june]
            subdfs.append(subdf)
        sizeId=pd.concat(subdfs,axis=1)
        sizeId.to_csv(path)
        return sizeId
    else:
        sizeId=pd.read_csv(path,index_col=0)
        sizeId.index=cleanStockId(sizeId.index)
        return sizeId

def getBtmId(btmNum,recal=False):
    path = r'D:\quantDb\researchTopics\fama\btmId_%s.csv' % btmNum
    if btmNum==3:
        btmNum=[0.3,0.7] #use break points to form the portfolios
    if recal or not os.path.exists(path):
        indicator=getIndicator()
        mkt=getMkt()
        Accpers = sorted(indicator['Accper'].unique().tolist())
        yearends = [Accper for Accper in Accpers if Accper.split('-')[1] == '12']

        subdfs = []
        for yearend in yearends:
            december = yearend[:-3]
            tmpdf = pd.DataFrame()

            bvdf = indicator[indicator['Accper'] == yearend]
            bvdf = bvdf.set_index('Stkcd')
            tmpdf['bv'] = bvdf['F091001A']

            mvdf = mkt[mkt['Trdmnt'] == december]  # use the ME of year t-1
            mvdf = mvdf.set_index('Stkcd')

            tmpdf['mv'] = mvdf['Mclsprc']
            tmpdf = tmpdf.dropna(axis=0,how='any')  # TODO: if there is no mv drop this stock,how about using the data before this report?
            tmpdf['btm'] = tmpdf['bv'] / tmpdf['mv']  # TODO: delete the stocks with bv smaller than 0?
            # TODO:delete the stocks listed in latest 2 years?
            tmpdf['btmId'] = mathu.getPortId(tmpdf['btm'], btmNum)
            btmId = tmpdf[['btmId']]
            btmId.columns=[december]
            subdfs.append(btmId)
        btmId=pd.concat(subdfs,axis=1)
        btmId.to_csv(path)
        return btmId
    else:
        btmId=pd.read_csv(path,index_col=0)
        btmId.index=cleanStockId(btmId.index)
        return btmId

# getSizeId(sizeNum=2)
# getBtmId(btmNum=3)
#
# getSizeId(sizeNum=5)
# getBtmId(btmNum=5)

def getPortId(sizeNum,btmNum,recal=False):
    path=r'D:\quantDb\researchTopics\fama\portId_%s_%s.csv'%(sizeNum,btmNum)
    if not os.path.exists(path) or recal:
        sizeId=getSizeId(sizeNum)
        btmId=getBtmId(btmNum)

        subdfs = []
        for year in range(1992, 2017):  # start from june of 1992,since there was too little stocks in december of 1991
            june = str(year) + '-06'
            december = str(year - 1) + '-12'

            idDf = pd.DataFrame()
            idDf['sizeId'] = sizeId[june]
            idDf['btmId'] = btmId[december]

            idDf = idDf.dropna(axis=0, how='any')
            idDf['group'] = idDf['sizeId'] * 10 + idDf['btmId']
            # groups=idDf['group'].unique().tolist()

            validMonths = [str(year) + '-0' + str(i) for i in
                           range(7, 10)]  # the valid month is from july of year t to june of year t+1
            validMonths += [str(year) + '-10', str(year) + '-11', str(year) + '-12']
            validMonths += [str(year + 1) + '-0' + str(i) for i in
                            range(1, 7)]  # notice: there is no data for 2017-04,2017-05....

            for month in validMonths:
                if month.split('-')[0] == '2017' and int(month.split('-')[1]) >= 4:
                    break
                subdf = pd.DataFrame()
                subdf[month] = idDf['group']
                subdfs.append(subdf)
        portId= pd.concat(subdfs, axis=1)
        portId.to_csv(path)
        return portId
    else:
        portId=pd.read_csv(path,index_col=0)
        portId.index=cleanStockId(portId.index)
        return portId

def getPortSize(sizeNum,btmNum):
    portId=getPortId(sizeNum,btmNum)
    portSize=pd.DataFrame()
    for i in range(portId.shape[1]):
        portSize.loc[portId.columns[i],'minNum']=portId.iloc[:,i].value_counts().min()
        portSize.loc[portId.columns[i],'totalNum']=portId.iloc[:,i].count().sum()
    portSize.to_csv(r'D:\quantDb\researchTopics\fama\portSize_%s_%s.csv'%(sizeNum,btmNum))

# getPortSize(2,3)
# getPortSize(5,5)

def getSMBandHML(recal=False):
    path=r'D:\quantDb\researchTopics\fama\factor.csv'
    if recal or not os.path.exists(path):
        mkt=getMkt()
        portId=getPortId(2,3)

        factor = pd.DataFrame(columns=['smb', 'hml'])
        months=portId.columns.tolist()[24:]
        for month in months:



            submkt=mkt[mkt['Trdmnt']==month]

            aa=portId[portId[month]==11].index.tolist()
            ab=portId[portId[month]==12].index.tolist()
            ac=portId[portId[month]==13].index.tolist()

            ba=portId[portId[month]==21].index.tolist()
            bb=portId[portId[month]==22].index.tolist()
            bc=portId[portId[month]==23].index.tolist()


            aaRet=pandasu.mean_self(submkt[submkt['Stkcd'].isin(aa)],gtaSettings.retType,gtaSettings.mvType)
            abRet=pandasu.mean_self(submkt[submkt['Stkcd'].isin(ab)],gtaSettings.retType,gtaSettings.mvType)
            acRet=pandasu.mean_self(submkt[submkt['Stkcd'].isin(ac)],gtaSettings.retType,gtaSettings.mvType)

            baRet=pandasu.mean_self(submkt[submkt['Stkcd'].isin(ba)],gtaSettings.retType,gtaSettings.mvType)
            bbRet=pandasu.mean_self(submkt[submkt['Stkcd'].isin(bb)],gtaSettings.retType,gtaSettings.mvType)
            bcRet=pandasu.mean_self(submkt[submkt['Stkcd'].isin(bc)],gtaSettings.retType,gtaSettings.mvType)

            smb=(aaRet+abRet+acRet)/3.0-(baRet+bbRet+bcRet)/3.0
            hml=(acRet+bcRet)/2.0-(aaRet+baRet)/2.0
            factor.loc[month]=[smb,hml]
            print month
        factor.to_csv(path)
        return factor
    else:
        factor=pd.read_csv(path,index_col=0)
        return factor

def getPortCounts(sizeNum,btmNum):
    portId=getPortId(sizeNum,btmNum)
    counts=[]
    for i in range(portId.shape[1]):
        count=portId.iloc[:,i].value_counts()
        counts.append(count)
    portCounts=pd.concat(counts,axis=1)
    portCounts=portCounts.fillna(0)
    portCounts.loc['min']=portCounts.min()
    portCounts.loc['max']=portCounts.max()
    portCounts.loc['total']=portCounts.sum()
    portCounts.to_csv(r'D:\quantDb\researchTopics\fama\portCounts_%s_%s.csv'%(sizeNum,btmNum))

# _=getPortCounts(2,3)
# _=getPortCounts(5,5)

def getPortRet(recal=False):
    path = r'D:\quantDb\researchTopics\fama\portRet.csv'
    if recal or not os.path.exists(path):
        mkt = getMkt()
        mkt = mkt.sort_values(['Trdmnt', 'Stkcd'],
                              ascending=[True, True])  # be sure to sort on both the date and stock code
        mkt = mkt.reset_index()
        group1 = mkt.groupby('Stkcd')

        mkt['weight'] = group1[gtaSettings.mvType].shift(1)

        portId = getPortId(5, 5)
        months = portId.columns.tolist()
        months = months[months.index('1995-07'):]
        ports = np.sort([p for p in portId[months[0]].unique() if not np.isnan(p)])

        portRet = pd.DataFrame()

        for month in months:
            submkt = mkt[mkt['Trdmnt'] == month]
            for port in ports:
                stocks = portId[portId[month] == port].index.tolist()
                ret = pandasu.mean_self(submkt[submkt['Stkcd'].isin(stocks)], gtaSettings.retType, 'weight')
                portRet.loc[month, port] = ret
                print month, port
        portRet.to_csv(path)
        return portRet
    else:
        portRet = pd.read_csv(path, index_col=0)
        return portRet

def getEret():
    portRet=getPortRet()
    rf=getRf()
    portEret=portRet.sub(rf['rf'],axis=0)
    portEret=portEret.dropna(axis=0,how='all')
    return portEret

# eret=getEret()


#validate factor return
def validateFactorRet():
    gtaff3=getFama3()
    myFactor=getSMBandHML()

    ressetFactor=ressetApi.getFama3()
    ressetFactor=ressetFactor.set_index('Date')
    ressetFactor=ressetFactor[['Smb_tmv','Hml_tmv','Rmrf_tmv']]
    ressetFactor.columns=['smb','hml','rp']
    ressetFactor.index=['-'.join(ind.split('-')[:2]) for ind in ressetFactor.index]
    print ressetFactor.head()


    gtaFactor = gtaff3.set_index('TradingMonth')
    del gtaFactor.index.name
    gtaFactor = gtaFactor[['SMB1', 'HML1', 'RiskPremium1']]
    gtaFactor.columns = ['smb', 'hml', 'rp']


    df = pd.DataFrame()
    df['mysmb'] = myFactor['smb']
    df['myhml'] = myFactor['hml']
    df['myrp'] = getRm()['rm']-getRf()['rf']
    df['gtasmb'] = gtaFactor['smb']
    df['gtahml'] = gtaFactor['hml']
    df['gtarp'] = gtaFactor['rp']
    df['rtsmb']=ressetFactor['smb']
    df['rthml']=ressetFactor['hml']
    df['rtrp']=ressetFactor['rp']

    ax1 = df[['mysmb', 'gtasmb', 'rtsmb']].cumsum().plot()
    ax2 = df[['myhml', 'gtahml', 'rthml']].cumsum().plot()
    ax3 = df[['myrp', 'gtarp', 'rtrp']].cumsum().plot()

    fig1 = ax1.get_figure()
    fig2 = ax2.get_figure()
    fig3 = ax3.get_figure()

    fig1.savefig(R'D:\quantDb\researchTopics\fama\validation\fig1.png')
    fig2.savefig(R'D:\quantDb\researchTopics\fama\validation\fig2.png')
    fig3.savefig(R'D:\quantDb\researchTopics\fama\validation\fig3.png')

#validate rm
def validateRm():
    myrm = getRm()
    rsrm = ressetApi.getRm()
    rsrm = rsrm.set_index('Date')
    rsrm.index = [extractDate(ind) for ind in rsrm.index]
    rsrm.index = [ind[:-3] for ind in rsrm.index]

    df = pd.DataFrame()
    df['myrm'] = myrm['rm']
    df['rsrm'] = rsrm['Mcrettmv']
    ax = df.cumsum().plot()
    fig=ax.get_figure()
    fig.savefig(r'D:\quantDb\researchTopics\fama\validation\rm.png')

#validate portfolio return
def validatePortRet():
    pr0=getPortRet()
    rs=ressetApi.getPortRet()
    rs['Date']=[d[:-3] for d in rs['Date']]

    months=pr0.index.tolist()
    pr1=pd.DataFrame()

    for month in months:
        tmpdf=rs[rs['Date']==month]
        for s in rs['Sizeflg'].unique():
            for b in rs['BMflg'].unique():
                pr1.loc[month,s*10+b]=tmpdf[(tmpdf['Sizeflg']==s) & (tmpdf['BMflg']==b)]['Pmonret_tmv'].values[0]
        print month

    pr1=pr1.reindex_axis(sorted(pr1.columns),axis=1)

    for portId in pr1.columns:
        tmpdf=pd.DataFrame()
        tmpdf['pr0']=pr0[portId]
        tmpdf['pr1']=pr1[portId]
        ax=tmpdf.cumsum().plot(title=portId)
        fig=ax.get_figure()
        fig.savefig(r'D:\quantDb\researchTopics\fama\validation\portRet\%s.png'%portId)

    avg0=pr0.mean().values.reshape((5,5))
    avg1=pr1.mean().values.reshape((5,5))

    df0=pd.DataFrame(avg0,index=range(1,6),columns=range(1,6))
    df0.index.name='size'
    df1=pd.DataFrame(avg1,index=range(1,6),columns=range(1,6))
    df1.index.name='size'

    df0.to_csv(r'D:\quantDb\researchTopics\fama\portAvgRet.csv')
    df1.to_csv(r'D:\quantDb\researchTopics\fama\portAvgRet_resset.csv')

#TODO: 3D bar
# from mpl_tooltiks.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import numpy as np
#
# fig=plt.figure()
#
# ax=fig.add_subplot(111,projection='3d')
# xpos=range(1,11)
# ypos=np.random.shuffle(range(2,8))
#
# zpos=[0]*10
# dx=np.ones(10)
# dy=np.ones(10)
#
# dz=range(1,11)
#
# ax.bar3d(xpos,ypos,zpos,dx,dy,dz,color='#00ceaa')
# plt.show()


#compare the regression result

#=====================================regression========================================
def regress():
    # Fama French 1993 table 3
    eret=getEret()
    rm=getRm()
    rf=getRf()
    factor=getSMBandHML()

    coef = pd.DataFrame(columns=['const', 'smb', 'hml', 'rp'])
    t = pd.DataFrame(columns=['const', 'smb', 'hml', 'rp'])
    r2 = pd.Series()

    errorDfs = []

    for groupId in eret.columns:
        tmpdf = pd.DataFrame()
        tmpdf['eret'] = eret[groupId]
        tmpdf['smb'] = factor['smb']
        tmpdf['hml'] = factor['hml']
        tmpdf['rp'] = rm['rm'] - rf['rf']

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

    coef.to_csv(r'D:\quantDb\researchTopics\fama\regression\coef.csv')
    t.to_csv((r'D:\quantDb\researchTopics\fama\regression\t.csv'))
    r2.to_csv((r'D:\quantDb\researchTopics\fama\regression\r2.csv'))
    errorDf.to_csv(r'D:\quantDb\researchTopics\fama\regression\error.csv')

################################################################
################################################################
################################################################
################################################################
################################################################
################################################################
################################################################

def readFromSrc(tbname):
    df=pd.read_csv(os.path.join(r'D:\zht\database\quantDb\sourceData\gta\data\csv',tbname+'.csv'))
    return df

#market data---------daily----------------------------------
def get_mktRetD(recal=False):
    '''
    daily market return
    the market refer to all the A-share stocks and the stocks in Growth Enterprise Market

    Returns:

    '''
    newName = 'mktRetD'
    path=os.path.join(processedPath,newName+'.csv')
    if os.path.exists(path) and recal==False:
        df=pd.read_csv(path,index_col=0,parse_dates=True)
        return df
    else:
        tbname='TRD_Cndalym'
        indVar='Trddt'

        targetVar='Cdretwdos'#考虑现金红利再投资的综合日市场回报率(流通市值加权平均法)
        q1='Markettype == 21'#21=综合A股和创业板

        df=readFromSrc(tbname)
        df=filterDf(df,q1)

        df=df.set_index(indVar)
        df=df.sort_index()
        df=df[[targetVar]]
        del df.index.name
        df.columns=[newName]

        df.index=pd.to_datetime(df.index)
        df.to_csv(path)
        return df

# get_mktRetD(recal=True)

def get_mktRetM(recal=False):
    newName='mktRetM'
    path=os.path.join(processedPath,newName+'.csv')
    if os.path.exists(path) and recal==False:
        df=pd.read_csv(path,index_col=0,parse_dates=True)
        return df
    else:
        tbname='TRD_Cnmont'
        indVar='Trdmnt'

        targetVar='Cmretwdos'#考虑现金红利再投资的综合日市场回报率(流通市值加权平均法)
        q1='Markettype == 21'#21=综合A股和创业板

        df=readFromSrc(tbname)
        df=filterDf(df,q1)

        df=df.set_index(indVar)
        df=df.sort_index()
        df=df[[targetVar]]
        del df.index.name
        df.columns=[newName]

        df.index = pd.to_datetime(df.index)
        df = df.resample('M').last()
        df.to_csv(path)
        return df

def get_stockRetD(recal=False):
    '''
    stock daily return with dividend
    Returns:dataframe

    '''
    path=os.path.join(processedPath,'stockRetD.csv')
    if os.path.exists(path) and recal==False:
        df=pd.read_csv(path,index_col=0,parse_dates=True)
        return df
    else:
        tbname='TRD_Dalyr'
        targetVar='Dretwd'#考虑现金红利再投资的收益

        df=readFromSrc(tbname)
        df=df[['Stkcd','Trddt','Dretwd']]

        m=flatten2panel(df,'Trddt','Stkcd',targetVar)
        m.index=pd.to_datetime(m.index)
        m.to_csv(path)
        return m

def get_stockCloseD(recal=False):
    path=os.path.join(processedPath,'stockCloseD.csv')
    if os.path.exists(path) and recal==False:
        df=pd.read_csv(path,index_col=0)
        return df
    else:
        tbname='TRD_Dalyr'
        targetVar='Clsprc'
        df=readFromSrc(tbname)
        df=flatten2panel(df,'Trddt','Stkcd',targetVar)
        df.to_csv(path)
        return df

#market data----------monthly---------------------------------
'''
there is no filter query for market data,but for those
financial data,the filter query is needed.
'''
def get_stockRetM(recal=False):
    '''
    monthly stock return with dividend

    Args:
        recal: if True,recalculate the indicator

    Returns:

    '''
    path=os.path.join(processedPath,'stockRetM.csv')
    if os.path.exists(path) and recal==False:
        df=pd.read_csv(path,index_col=0,parse_dates=True)
        return df
    else:
        tbname='TRD_Mnth'
        var='Mretwd'#考虑现金红利再投资的收益
        ind='Trdmnt'
        col='Stkcd'
        df=readFromSrc(tbname)
        df=flatten2panel(df,ind,col,var)

        df.index=pd.to_datetime(df.index)
        df=df.resample('M').last()
        df.to_csv(path)
        return df

def get_sizeM(recal=False):
    '''
    monthly stock tradable market value

    Args:
        recal:

    Returns:

    '''
    path=os.path.join(processedPath,'sizeM.csv')
    if os.path.exists(path) and recal==False:
        df=pd.read_csv(path,index_col=0,parse_dates=True)
        return df
    else:
        tbname='TRD_Mnth'
        var='Msmvosd' #月个股流通市值
        ind='Trdmnt'
        col='Stkcd'
        df=readFromSrc(tbname)
        df=flatten2panel(df,ind,col,var)
        df.index = pd.to_datetime(df.index)
        df = df.resample('M').last()
        df.to_csv(path)
        return df

#data set -------------------------------------------------------
def get_nfc():
    '''
    non-financial stock codes
    :return:
    '''
    tbname='TRD_Co'
    df=pd.read_csv(os.path.join(sp,tbname+'.csv'))
    nf=df[df['Indcd']!=1]
    nf=nf.reset_index()
    nf=nf[['Stkcd']]
    return nf

#financial data from report--------------------------------------
#TODO: move the function from getData in assetPricing project to this script


def get_rf(freq):
    '''
    parse risk free rate from the database
    Args:
        freq: D (daily),W (weekly),M (monthly)

    Returns:

    '''
    dic={'D':'Nrrdaydt','W':'Nrrwkdt','M':'Nrrmtdt'}

    tname = 'TRD_Nrrate'
    src = readFromSrc(tname)
    src=src[src['Nrr1']=='NRI01']#NRI01=定期-整存整取-一年利率；TBC=国债票面利率
    src=src.set_index('Clsdt')
    del src.index.name

    rf=src[[dic[freq]]][2:]#delete the first two rows
    rf.columns=['rf']

    rf.index=pd.to_datetime(rf.index)
    if freq in ['W','M']:
        rf=rf.resample(freq).last()

    return rf

































