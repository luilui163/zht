#-*-coding: utf-8 -*-
#author:tyhj
#calFactors.py 2017/8/17 10:55
import pandas as pd
import numpy as np
import os

from zht.data.resset import ressetApi
from zht.data.gta import gtaApi
from zht.util import pandasu
from zht.util.dfFilter import filterDf
from zht.util.mathu import *


from params import *
from main import get_portRet

def get_ff3Factors():
    '''
    get smb and hml in ff3 model
    Returns:

    '''
    #TODO:think about weighted average rather than equal weighted
    def func1(x):#factor return
        return (x[13]+x[23])/2-(x[11]+x[21])/2
    def func2(x):#smb
        return (x[11]+x[12]+x[13])/3-(x[21]+x[22]+x[23])/3

    model='2x3'
    vars=['size','btm']
    portRet=get_portRet(vars,model)

    portRet.columns=[int(float(col)) for col in portRet.columns]
    hml=portRet.apply(func1,axis=1)#factor return

    smb=portRet.apply(func2,axis=1)

    # hml.to_csv(os.path.join(ff3FactorP,'hml.csv'))
    # smb.to_csv(os.path.join(ff3FactorP,'smb.csv'))
    return smb,hml

smb,hml=get_ff3Factors()
df=pd.DataFrame()
df['smb']=smb
df['hml']=hml
df.cumsum().plot()





#momentum
def get_carhart4():
    '''
    carhart momentum factor is constructed as the equal-weighted
    average of firms with the highest 30 percent eleven-month returns
    lagged one month minus the equal-weight average of firms with the
    lowest 30 percent eleven-month returns lagged one month.

    reference:
        On persistence in mutual fund performance,Carhart 1997
    '''
    mom=ressetApi.getMomentum()
    carhartMom=mom['MomFac_11M_Eq']
    carhartMom.to_csv(os.path.join(factorRetPath,'carhartMom.csv'))

def get_liqSen():
    '''
    calculate the marketwide liquidity indicator (lt) and stocks' sensitivity respect to
    'lt',adjusted for exposures to fama french three factors.

    "Liquidity Risk and Expected Stock Returns",by Lubos Pastor,2003

    Returns:

    '''
    mktRet=gtaApi.get_mktRetD()
    ret=gtaApi.get_stockRetD()
    # the volume is measured in millions of dollars as in the paper,
    # here we use million Chinese Yuan
    vol=gtaApi.get_stockVolD()/1000000

    close=gtaApi.get_stockCloseD()

    mktRet,ret,vol=pandasu.get_inter_index([mktRet,ret,vol])
    excessRet=ret.sub(mktRet.iloc[:,0],axis=0)
    sign=np.sign(excessRet)

    monthStarts,monthEnds=pandasu.getMonthStartAndEnd(mktRet)
    monthStarts=monthStarts[1:-1]
    monthEnds=monthEnds[1:-1]

    def _get_validStocks(monthEnd):
        '''
        Stocks with share prices less than $5 and greater than $1000
        at the end of the previous month are filtered out.

        Args:
            monthEnd:

        Returns:

        '''
        closeprice=close.loc[monthEnd,:]
        stocks=closeprice[(5.0<closeprice) & (closeprice<1000.0)].index.tolist()
        return stocks

    gammait=pd.DataFrame()
    for start,end in zip(monthStarts,monthEnds):
        validStocks=_get_validStocks(end)

        retsub=ret.loc[start:end,validStocks]
        volsub=vol.loc[start:end,validStocks]

        excessRetsub=excessRet.loc[start:end,validStocks]
        signsub=sign.loc[start:end,validStocks]

        for stock in validStocks:
            regdf=pd.DataFrame()
            regdf['y']=excessRetsub[stock].shift(-1)#the dependable variable is
            regdf['x1']=retsub[stock]
            regdf['x2']=signsub[stock]*volsub[stock]
            regdf=regdf.dropna(axis=0,how='any')
            if regdf.shape[0]>10:
                #the threshold in the pastor's paper is 15.Since it will filter out a lot of samples,we lower our threshold.
                slope,t,r2,resid=pandasu.reg(regdf)
                gammait.loc[start[:-3],stock]=slope[2]
        print start[:-3]

    # gammait=pd.read_csv(os.path.join(idp,'liq.csv'),index_col=0)
    gammait=pandasu.winsorize(gammait,axis=0)
    # TODO:there are some extremely outliers to be filtered out
    # gammait.to_csv(os.path.join(idp,'liq.csv'))

    gammat = gammait.mean(axis=1)

    deltaGammat=pd.Series()
    m1=0
    mts=pd.Series()
    months=gammait.index.tolist()
    delta=gammait-gammait.shift(1)
    for i in range(1,len(months)):
        #months[i] denotes t,and months[i-1] denotes t-1
        tickers=delta.loc[months[i]].dropna().index.tolist()
        date=[m for m in monthEnds if m.startswith(months[i-1])][0]#the end of the month t-1
        if i==1:
            m1=vol.loc[date,tickers].sum()
        #mt is the total value at the end of month t-1 of the stocks included
        #in the average in montht,and month 1 corresponds to the first month.
        mt=vol.loc[date,tickers].sum()
        mts[months[i]]=mt
        deltaGammat[months[i]]=mt/m1*delta.loc[months[i]].mean()
        print months[i]

    regdf=pd.DataFrame()
    regdf['y']=deltaGammat
    regdf['x1']=deltaGammat.shift(1)
    regdf['x2']=mts.shift(1)/m1*gammat.shift(1)
    regdf=regdf.dropna(axis=0,how='any')
    slope,t,r2,resid=pandasu.reg(regdf)
    mut=pd.Series(resid,index=regdf.index)
    lt=mut/10.0#adjust the magnitude of the data,which do not affect the result

    lt=lt.fillna(method='ffill')#there are several NaNs,fill them
    lt.to_csv(os.path.join(idp,'liquidity.csv'))

    eret=pd.read_csv(os.path.join(tmpp,'eret.csv'),index_col=0)
    smb=pd.read_csv(os.path.join(factorRetPath,'2x3_smb.csv'),index_col=0)
    hml=pd.read_csv(os.path.join(factorRetPath,'2x3_hml.csv'),index_col=0)
    rp=pd.read_csv(os.path.join(bdp,'rp.csv'),index_col=0)
    #liquidity sensitivity
    liqSen=pd.DataFrame()

    for count,col in enumerate(eret.columns):
        regdf=pd.DataFrame()
        regdf['y']=eret[col]
        regdf['x1']=lt/10000000.0
        regdf['x2']=smb['smb']
        regdf['x3']=hml['hml']
        regdf['x4']=rp['rp']
        for i in range(60,regdf.shape[0]):
            sub=regdf.iloc[i-60:i,:]
            sub=sub.dropna(axis=0,how='any')
            if sub.shape[0]>36:
                slope,t,r2,resid=pandasu.reg(sub)
                liqSen.loc[regdf.index[i],col]=slope[1]
        print count
        #TODO:using rolling method.
        # pd.rolling_apply(regdf,window=300,func=func,min_periods=150)
        # model=regdf.rolling(window=300,min_periods=150).apply(func)
    liqSen.to_csv(os.path.join(idp,'liqSen.csv'))

def get_hxz4Factors():
    '''
    Hou,Xue and Zhang,q-4 model

    data source:
    I/A:
        method 1:
            total asset:
            TBName:FS_Combas
            Fldname:A001000000

            I/A=diff(ta)/ta_(t-1)

        method 2:
            TBName:FI_T8
            Fldname:F080602A

    ROE:
        TBName:FI_T5
        Fldname:F050501B

    '''
    for tbname,vname,fname in [('FI_T8','F080602A','I2A'),('FI_T5','F050501B','ROE')]:
        q='Typrep == A'
        df=gtaApi.readFromSrc(tbname)
        df=filterDf(df,q)

        indvar='Accper'
        colvar='Stkcd'
        mydf=pandasu.flatten2panel(df,indvar,colvar,vname)
        mydf.to_csv(os.path.join(hxz4FactorP,fname+'.csv'))


    #get report date
    tbname='IAR_Forecdt'
    df=gtaApi.readFromSrc(tbname)
    print df.head()


    indvar='Accper'
    colvar='Stkcd'
    vname='Firforecdt'
    fname='reportDate'

    mydf=pandasu.flatten2panel(df,indvar,colvar,vname)
    mydf.to_csv(os.path.join(hxz4FactorP,fname+'.csv'))


    #get size ids
    size=pd.read_csv(os.path.join(tmpp,'size.csv'),index_col=0)
    validInd=[ind for ind in size.index if ind.endswith('06')]
    size=size.reindex(index=validInd)
    # size=size.loc[validInd]
    sizeId=getSortedPortId(size,2)
    sizeId.index=[ind.split('-')[0]+'-07' for ind in sizeId.index]#in july,use the size in the end of june.
    newIndex=pd.date_range(sizeId.index[0],str(int(sizeId.index[-1].split('-')[0])+1)+'-07',freq='M')
    newIndex=[d.strftime('%Y-%m') for d in newIndex]
    sizeId=sizeId.reindex(index=newIndex)
    sizeId=sizeId.ffill()
    sizeId.to_csv(os.path.join(hxz4FactorP,'sizeId.csv'))

    #get I/A ids
    i2a=pd.read_csv(os.path.join(hxz4FactorP,'I2A.csv'),index_col=0)
    i2a.index=[ind[:-3] for ind in i2a.index]
    validMonth=[ind for ind in i2a.index if ind.endswith('12')]
    i2a=i2a.reindex(index=validMonth)
    i2aId=getSortedPortId(i2a,[0.3,0.7])
    i2aId.index=[str(int(ind.split('-')[0])+1)+'-07' for ind in i2aId.index]
    newIndex=pd.date_range(i2aId.index[0],str(int(i2aId.index[-1].split('-')[0])+1)+'-07',freq='M')
    newIndex=[d.strftime('%Y-%m') for d in newIndex]
    i2aId=i2aId.reindex(index=newIndex)
    i2aId=i2aId.ffill()
    i2aId.to_csv(os.path.join(hxz4FactorP,'i2aId.csv'))

    #get roe id
    roe=pd.read_csv(os.path.join(hxz4FactorP,'ROE.csv'),index_col=0)
    reportDate=pd.read_csv(os.path.join(hxz4FactorP,'reportDate.csv'),index_col=0)
    reportDate,roe=pandasu.get_outer_frame([reportDate,roe])

    drs=pd.date_range(start=roe.index[0],end=roe.index[-1],freq='M')
    drs=[d.strftime('%Y-%m') for d in drs]

    roeLatest=pd.DataFrame(index=drs,columns=roe.columns)

    for col in roe.columns:
        for ind in roe.index:
            if not pd.isnull(roe.loc[ind,col]):
                if not pd.isnull(reportDate.loc[ind,col]):
                    announceDate=reportDate.loc[ind,col]
                    startMonth=(pd.Timestamp(announceDate)+pd.DateOffset(months=1)).strftime('%Y-%m')
                    roeLatest.loc[startMonth,col]=roe.loc[ind,col]
                else:
                    startMonth=(pd.Timestamp(ind)+pd.DateOffset(months=7)).strftime('%Y-%m')
                    roeLatest.loc[startMonth,col]=roe.loc[ind,col]
        print col

    roeId=getSortedPortId(roeLatest,[0.3,0.7])
    roeId=roeId.ffill()
    roeId.to_csv(os.path.join(hxz4FactorP,'roeId.csv'))


    sizeId,i2aId,roeId=pandasu.get_inter_frame([sizeId,i2aId,roeId])
    #the first number(1 or 2) denotes size portfolio,the second number(1,2,o4 3) denotes I/A portfolio
    #and the third number(1,2,or 3) denotes ROE portfolio
    portId=sizeId*100+i2aId*10+roeId
    portId=portId.T
    ret=pd.read_csv(os.path.join(bdp,'ret.csv'),index_col=0)
    weight=pd.read_csv(os.path.join(bdp,'weight.csv'),index_col=0)

    ports=np.sort([p for p in np.unique(sizeId.fillna(0.0)) if p!=0.0])

    portRet=pd.DataFrame()
    for month in portId.columns:
        for port in ports:
            stocks=portId[portId[month]==port].index.tolist()
            if month in ret.index.tolist():
                try:
                    tmp=pd.DataFrame()
                    tmp['ret']=ret.loc[month,stocks]
                    tmp['weight']=weight.loc[month,stocks]
                    tmp=tmp.dropna(axis=0,how='any')
                    pr=pandasu.mean_self(tmp,'ret','weight')
                    portRet.loc[month,port]=pr
                except KeyError:
                    portRet.loc[month,port]=np.NaN
            else:
                portRet.loc[month,port]=np.NaN
        print month

    portRet.columns=[int(col) for col in portRet.columns]
    portRet.to_csv(os.path.join(hxz4FactorP,'portRet.csv'))


    #get factor return

    #for size:small-minus-big
    bigCols=[col for col in portRet.columns if col/100==2]
    smallCols=[col for col in portRet.columns if col/100==1]
    smbRet=portRet[smallCols].mean(axis=1)-portRet[bigCols].mean(axis=1)

    #for I/A:low-minus-high
    highCols1=[col for col in portRet.columns if (col/10)%10==3]
    lowCols1=[col for col in portRet.columns if (col/10)%10==1]
    i2aRet=portRet[lowCols1].mean(axis=1)-portRet[highCols1].mean(axis=1)

    #for ROE:high-minus-low
    highCols2=[col for col in portRet.columns if col%10==3]
    lowCols2=[col for col in portRet.columns if col%10==1]
    roeRet=portRet[highCols2].mean(axis=1)-portRet[lowCols2].mean(axis=1)

    smbRet.to_csv(os.path.join(hxz4FactorP,'rsmb.csv'))
    i2aRet.to_csv(os.path.join(hxz4FactorP,'ria.csv'))
    roeRet.to_csv(os.path.join(hxz4FactorP,'rroe.csv'))


# get_hxz4Factors()


