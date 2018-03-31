#-*-coding: utf-8 -*-
#author:tyhj
#classicalModels.py 2017/9/19 18:35


import pandas as pd
import os

from zht.data.resset import ressetApi
from zht.data.gta import gtaApi
from zht.util import pandasu
from zht.util.dfFilter import filterDf
from zht.util.mathu import *
from zht.util.pandasu import getSortedPortId

from tools import *
from params import *

def get_capm():
    df=pd.DataFrame()
    df['rp']=pd.read_csv(os.path.join(bdp,'rp.csv'),index_col=0)['rp']
    return df

def get_ff3():
    #TODO:no financial stocks
    '''
    get smb and hml in ff3 model
    :return:
    '''
    vars=['size','btm']
    model='2x3'
    f1,f2=intersectionFactorRet(vars,model)
    smb,hml=-f1,f2

    df=get_capm()
    df['smb']=smb
    df['hml']=hml

    return df

def get_carhart4():
    '''
    carhart momentum factor is constructed as the equal-weighted
    average of firms with the highest 30 percent eleven-month returns
    lagged one month minus the equal-weight average of firms with the
    lowest 30 percent eleven-month returns lagged one month.

    reference:
        On persistence in mutual fund performance,Carhart 1997
    '''
    df=get_ff3()

    mom=ressetApi.getMomentum()
    carhartMom=mom['MomFac_11M_Eq']

    df['mom']=carhartMom

    return df

def get_liq4():
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
    # lt.to_csv(os.path.join(idp,'liquidity.csv'))

    eret=pd.read_csv(os.path.join(tmpp,'eret.csv'),index_col=0)

    ff3=get_ff3()

    #liquidity sensitivity
    liqSen=pd.DataFrame()

    for count,col in enumerate(eret.columns):
        regdf=pd.DataFrame()
        regdf['y']=eret[col]
        regdf['x1']=lt/10000000.0
        regdf['x2']=ff3['smb']
        regdf['x3']=ff3['hml']
        regdf['x4']=ff3['rp']
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
    # liqSen.to_csv(os.path.join(idp,'liqSen.csv'))

    marketLiquidity=gammat
    liquidityInnovation=lt
    liquiditySensitivity=liqSen

    liq4=get_ff3()
    liq4['liq']=marketLiquidity

    marketLiquidity.to_csv(os.path.join(liq4p, 'marketliquidity.csv'))
    liquidityInnovation.to_csv(os.path.join(liq4p, 'liquidityInnovation.csv'))
    liquiditySensitivity.to_csv(os.path.join(liq4p, 'liquiditySensitivity.csv'))
    liq4.to_csv(os.path.join(liq4p,'liq4.csv'))

    return liq4,marketLiquidity,liquidityInnovation,liquiditySensitivity

def get_hxz4():
    '''
    Hou,Xue and Zhang,q-4 model

    rp is excess market return
    size is updated yearly at the June of each year.
    I/A is updated yearly at the June of each year.
    ROE is updated monthly at the beginning of each month using the data in most recent quarterly earnings anouncement.


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
    i2a=pd.DataFrame()
    roe=pd.DataFrame()
    for tbname,vname,fname in [('FI_T8','F080602A','I2A'),('FI_T5','F050501B','ROE')]:
        q='Typrep == A'
        df=gtaApi.readFromSrc(tbname)
        df=filterDf(df,q)

        indvar='Accper'
        colvar='Stkcd'
        if fname=='I2A':
            i2a=pandasu.flatten2panel(df,indvar,colvar,vname)
        elif fname=='ROE':
            roe=pandasu.flatten2panel(df,indvar,colvar,vname)

        # mydf=pandasu.flatten2panel(df,indvar,colvar,vname)
        # mydf.to_csv(os.path.join(hxz4FactorP,fname+'.csv'))


    #get report date
    tbname='IAR_Forecdt'
    df=gtaApi.readFromSrc(tbname)

    indvar='Accper'
    colvar='Stkcd'
    vname='Firforecdt'

    reportDate=pandasu.flatten2panel(df,indvar,colvar,vname)

    # mydf=pandasu.flatten2panel(df,indvar,colvar,vname)
    # mydf.to_csv(os.path.join(hxz4FactorP,fname+'.csv'))


    #get size ids
    sizeId=getIndicatorId('size',2)
    # sizeId.to_csv(os.path.join(hxz4FactorP,'sizeId.csv'))

    #get I/A ids
    # i2a=pd.read_csv(os.path.join(hxz4FactorP,'I2A.csv'),index_col=0)
    i2a.index=[ind[:-3] for ind in i2a.index]
    validMonth=[ind for ind in i2a.index if ind.endswith('12')]
    i2a=i2a.reindex(index=validMonth)
    i2aId=getSortedPortId(i2a,[0.3,0.7])
    i2aId.index=[str(int(ind[:4])+1)+'-07' for ind in i2aId.index]
    newIndex=pd.date_range(i2aId.index[0],str(int(i2aId.index[-1][:4])+1)+'-07',freq='M')
    newIndex=[d.strftime('%Y-%m') for d in newIndex]
    i2aId=i2aId.reindex(index=newIndex)
    i2aId=i2aId.ffill()
    # i2aId.to_csv(os.path.join(hxz4FactorP,'i2aId.csv'))

    #get roe id
    # roe=pd.read_csv(os.path.join(hxz4FactorP,'ROE.csv'),index_col=0)
    # reportDate=pd.read_csv(os.path.join(hxz4FactorP,'reportDate.csv'),index_col=0)
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
            print col,ind
    #TODO:build a module to get latest financial data by taking into announcement date into consideration.

    roeId=getSortedPortId(roeLatest,[0.3,0.7])
    roeId=roeId.ffill()
    # roeId.to_csv(os.path.join(hxz4FactorP,'roeId.csv'))


    sizeId,i2aId,roeId=pandasu.get_inter_frame([sizeId,i2aId,roeId])
    #the first number(1 or 2) denotes size portfolio,the second number(1,2,o4 3) denotes I/A portfolio
    #and the third number(1,2,or 3) denotes ROE portfolio
    portId=sizeId*100+i2aId*10+roeId

    portRet=calPortRet(portId)
    portRet.columns=[int(col) for col in portRet.columns]
    # portRet.to_csv(os.path.join(hxz4FactorP,'portRet.csv'))


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

    df=get_capm()
    df['smb']=smbRet
    df['i2a']=i2aRet
    df['roe']=roeRet

    return df

def get_ff5(model):
    '''
    refer to 'A five-factor asset pricing model' by Fama and French,2015

    for other analysis about ff5 refer to project assetPricing/main.py


    :param model:'2x2',or '2x3' or '2x4x4'
    :return:
    '''
    if model in ['2x2', '2x3']:
        vars = ['size', 'btm', 'op', 'inv']
        factorNames = ['smb', 'hml', 'rmw', 'cma']
        ind2name = {ind: name for ind, name in zip(vars, factorNames)}

        df = get_capm()
        smbs = pd.DataFrame()
        for var in ['btm', 'op', 'inv']:
            vars = ['size', var]
            f1, f2 = intersectionFactorRet(vars, model)

            smb = -f1
            smbs[var] = smb

            if var == 'inv':
                f2 = -f2  # for inv,it is low minus high
            df[ind2name[var]] = f2
        SMB = smbs.mean(axis=1)
        df['smb'] = SMB
        return df

    elif model == '2x2x2x2':
        vars = ['size', 'btm', 'op', 'inv']
        f1, f2, f3, f4 = intersectionFactorRet(vars, model)

        df = get_capm()
        df['smb'] = -f1  # low minus high
        df['hml'] = f2
        df['rmw'] = f3
        df['cma'] = -f4  # low minus high
        return df



if __name__=='__main__':
    capm=get_capm()
    ff3=get_ff3()
    carhart4=get_carhart4()

    liq4,_,_,_=get_liq4()
    hxz4=get_hxz4()
    ff5=get_ff5(model='2x2')

    capm.to_csv(os.path.join(bmp,'capm.csv'))
    ff3.to_csv(os.path.join(bmp,'ff3.csv'))
    carhart4.to_csv(os.path.join(bmp,'carhart4.csv'))
    liq4.to_csv(os.path.join(bmp,'liq4.csv'))
    hxz4.to_csv(os.path.join(bmp,'hxz4.csv'))
    ff5.to_csv(os.path.join(bmp,'ff5.csv'))

