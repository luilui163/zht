#-*-coding: utf-8 -*-
#author:tyhj
#dfApi.py 2017/7/28 11:07
import pandas as pd
import os
from zht.util import stru
from zht.util.dfFilter import filterDf
from zht.util.pandasu import mean_self
import numpy as np
from zht.util import mathu

def _getGTAdf1():
    dirpath=r'D:\quantDb\sourceData\gta\data\csv'

    tn='FS_Combas'
    df=pd.read_csv(os.path.join(dirpath,tn+'.csv'))
    df=df[df['Typrep']=='A'] #TODO 合并报表
    q='Accper endswith 12-31'
    df=filterDf(df,q)

    df['Stkcd']=stru.cleanStockId(df['Stkcd'])
    colnames=['Stkcd','Accper','A001000000','A003000000']

    df=df[colnames]
    df=df.rename(columns={'A001000000':'totalAsset','A003000000':'totshe'})
    df=df.sort_values(['Stkcd','Accper'],ascending=[True,True])
    df=df.set_index(['Stkcd','Accper'])
    return df

def _getGTAdf2():
    dirpath=r'D:\quantDb\sourceData\gta\data\csv'
    tn='FS_Comins'

    df = pd.read_csv(os.path.join(dirpath, tn + '.csv'))
    df = df[df['Typrep'] == 'A']  # TODO 合并报表
    q = 'Accper endswith 12-31'
    df = filterDf(df, q)

    df['Stkcd'] = stru.cleanStockId(df['Stkcd'])
    colnames=['Stkcd','Accper','B001101000','B001209000','B001210000','B001211000']
    df=df[colnames]
    df=df.rename(columns={'B001101000':'operIncom',
                          'B001209000':'operExp',
                          'B001210000':'admExp',
                          'B001211000':'finanExp'})
    df = df.sort_values(['Stkcd', 'Accper'], ascending=[True, True])
    df = df.set_index(['Stkcd', 'Accper'])
    return df

def get_OPandINV():
    df1=_getGTAdf1()
    df2=_getGTAdf2()

    df=pd.concat([df1,df2],axis=1)
    df[['operExp','admExp','finanExp']]=df[['operExp','admExp','finanExp']].fillna(0) #TODO:choose the fill method
    df['op']=(df['operIncom']-df['operExp']-df['admExp']-df['finanExp'])/df['totshe']
    df['inv']=df['totalAsset'].pct_change()
    OPandINV=df[['op','inv']]
    OPandINV.to_csv(r'D:\quantDb\researchTopics\ff5\data\OPandINV.csv')
    return OPandINV
#TODO:是否剔除银行股？

def get_totshe():
    dirpath = r'D:\quantDb\sourceData\gta\data\csv'

    tn = 'FS_Combas'
    df = pd.read_csv(os.path.join(dirpath, tn + '.csv'))
    df = df[df['Typrep'] == 'A']  # TODO 合并报表
    q = 'Accper endswith 12-31'
    df = filterDf(df, q)

    df['Stkcd'] = stru.cleanStockId(df['Stkcd'])
    colnames = ['Stkcd', 'Accper', 'A003000000']

    df = df[colnames]
    df = df.rename(columns={ 'A003000000': 'totshe'})
    df = df.sort_values(['Stkcd', 'Accper'], ascending=[True, True])
    df = df.set_index(['Stkcd', 'Accper'])
    df.to_csv(r'D:\quantDb\researchTopics\ff5\data\totshe.csv')

def getGTAdf(tn):
    dirpath = r'D:\quantDb\sourceData\gta\data\csv'
    df=pd.read_csv(os.path.join(dirpath,tn+'.csv'))
    return df

def get_Mretwd_and_Msmvosd():
    '''
    Mretwd:monthly return with dividend
    Msmvosd:monthly tradable market value
    :return:
    '''

    df=getGTAdf('TRD_Mnth')
    q='Markettype in [1,4,16]'
    df=filterDf(df,q)
    colnames=['Trdmnt','Stkcd','Mretwd','Msmvosd','Markettype']
    df=df[colnames]
    df['Stkcd']=stru.cleanStockId(df['Stkcd'])
    df=df.sort_values(['Trdmnt','Stkcd'])
    df=df.set_index(['Trdmnt','Stkcd'])
    df.to_csv(r'D:\quantDb\researchTopics\ff5\data\MretwdAndMsmvosd.csv')

def get_rf():
    df=getGTAdf('TRD_Nrrate')
    q='Nrr1 == NRI01' #TODO:TBC=国债票面利率
    df=filterDf(df,q)
    colnames=['Clsdt','Nrrmtdt']
    df=df.sort_values('Clsdt')

    df=df[colnames]
    df=df.set_index('Clsdt')

    dates=pd.date_range(df.index[0],df.index[-1],freq='D')
    dates=[d.strftime('%Y-%m-%d') for d in dates]

    newdf=pd.DataFrame(index=dates)
    newdf['Nrrmtdt']=df['Nrrmtdt']
    newdf=newdf.fillna(method='ffill')
    newdf=newdf.reset_index()
    newdf['month']=newdf['index'].apply(lambda x:'-'.join(x.split('-')[:-1]))

    avg=newdf.groupby('month').mean()
    avg=avg/100
    del avg.index.name
    avg.columns=['rf']
    avg.to_csv(r'D:\quantDb\researchTopics\ff5\data\rf.csv')

def get_rm():
    df=pd.read_csv(r'D:\quantDb\researchTopics\ff5\data\MretwdAndMsmvosd.csv')
    df=df.sort_values(['Stkcd','Trdmnt'])
    # df=df.set_index(['Stkcd','Trdmnt'])

    df['weight']=df.groupby('Stkcd')['Msmvosd'].shift(1) #TODO:important!!!! use last month's mv as weight,rather than current month

    # rm0=pd.DataFrame()
    # for month in df['Trdmnt'].unique().tolist():
    #     sub=df[df['Trdmnt']==month]
    #     sub=sub.dropna(axis=0,how='any')
    #     rm0.loc[month,'rm']=mean_self(sub,'Mretwd','Msmvosd')
    #     print month

    wm=lambda x:np.average(x,weights=df.loc[x.index,'weight'])
    df=df.dropna(axis=0,how='any')
    rm = df.groupby('Trdmnt').agg({'Mretwd':wm})
    rm.columns=['rm']
    del rm.index.name
    rm.to_csv(r'D:\quantDb\researchTopics\ff5\data\rm.csv')

def get_mv():
    df = getGTAdf('TRD_Mnth')
    q1 = 'Markettype in [1,4,16]'
    q2 = 'Trdmnt endswith 12'
    q=[q1,q2]
    df = filterDf(df, q)
    colnames = ['Trdmnt', 'Stkcd', 'Mclsprc']
    df = df[colnames]
    df['Stkcd'] = stru.cleanStockId(df['Stkcd'])
    df = df.sort_values(['Stkcd','Trdmnt'])
    df = df.set_index(['Stkcd','Trdmnt'])
    df=df.rename(columns={'Mclsprc':'mv'})
    df.to_csv(r'D:\quantDb\researchTopics\ff5\data\mv.csv')

def get_bv():
    df=getGTAdf('FI_T9')
    q1='Typrep == A'
    q2='Accper endswith 12-31'
    q=[q1,q2]
    df=filterDf(df,q)

    colnames=['Stkcd','Accper','F091001A']
    df=df[colnames]
    df['Stkcd']=stru.cleanStockId(df['Stkcd'])
    df=df.rename(columns={'F091001A':'bv'})
    df['Accper']=df['Accper'].apply(lambda x:'-'.join(x.split('-')[:-1]))

    df=df.sort_values(['Stkcd','Accper'])
    df=df.set_index(['Stkcd','Accper'])
    df.to_csv(r'D:\quantDb\researchTopics\ff5\data\bv.csv')

def get_btm():
    mv=pd.read_csv(r'D:\quantDb\researchTopics\ff5\data\mv.csv')
    bv=pd.read_csv(r'D:\quantDb\researchTopics\ff5\data\bv.csv')
    mv['Stkcd']=stru.cleanStockId(mv['Stkcd'])
    bv['Stkcd']=stru.cleanStockId(bv['Stkcd'])

    mv=mv.rename(columns={'Trdmnt':'month'})
    bv=bv.rename(columns={'Accper':'month'})

    mv=mv.set_index(['month','Stkcd'])
    bv=bv.set_index(['month','Stkcd'])

    df=pd.concat([mv,bv],axis=1)

    df=df.reset_index()

    df=df.dropna(axis=0,how='any')
    df['btm']=df['bv']/df['mv']
    df=df[['month','Stkcd','btm']]
    df=df.set_index('month')
    df.to_csv(r'D:\quantDb\researchTopics\ff5\data\btm.csv')

def get_sizeId(sizeNum):
    df=pd.read_csv(r'D:\quantDb\researchTopics\ff5\data\MretwdAndMsmvosd.csv')
    q='Trdmnt endswith 06'

    df=filterDf(df,q)[['Trdmnt','Stkcd','Msmvosd']]
    junes=sorted(df['Trdmnt'].unique().tolist())
    subdfs=[]
    for june in junes:
        sub=df[df['Trdmnt']==june]
        sub=sub.dropna(axis=0,how='any')
        sub.loc[:,'sizeId']=mathu.getPortId(sub['Msmvosd'],sizeNum)
        subdfs.append(sub)
        print june

    sizeId=pd.concat(subdfs,axis=0)
    sizeId=sizeId.set_index('Trdmnt')
    del sizeId.index.name
    del sizeId['Msmvosd']
    sizeId.to_csv(r'D:\quantDb\researchTopics\ff5\data\sizeId_%s.csv'%sizeNum)

def get_btmId(btmNum):
    path=r'D:\quantDb\researchTopics\ff5\data\btmId_%s.csv'%btmNum
    if btmNum==3:
        btmNum=[0.3,0.7]
    df=pd.read_csv(r'D:\quantDb\researchTopics\ff5\data\btm.csv')
    decembers=sorted(df['month'].unique().tolist())
    subdfs=[]
    for december in decembers:
        june=str(int(december.split('-')[0])+1)+'-06'
        sub=df[df['month']==december].copy()
        sub['month']=june
        sub=sub.dropna(axis=0,how='any')
        sub.loc[:,'btmId']=mathu.getPortId(sub['btm'],btmNum)
        subdfs.append(sub)
        print june
    btmId=pd.concat(subdfs,axis=0)
    btmId=btmId.set_index('month')
    del btmId.index.name
    del btmId['btm']
    btmId.to_csv(path)

def get_portId(sizeNum, btmNum):
    path = r'D:\quantDb\researchTopics\ff5\data\portId_%s_%s.csv' % (sizeNum, btmNum)

    sizeId = pd.read_csv(r'D:\quantDb\researchTopics\ff5\data\sizeId_%s.csv' % sizeNum, index_col=0)
    btmId = pd.read_csv(r'D:\quantDb\researchTopics\ff5\data\btmId_%s.csv' % btmNum, index_col=0)
    sizeId['Stkcd'] = stru.cleanStockId(sizeId['Stkcd'])
    btmId['Stkcd'] = stru.cleanStockId(btmId['Stkcd'])

    sizeId = sizeId.reset_index()
    btmId = btmId.reset_index()

    sizeId = sizeId.rename(columns={'index': 'month'})
    btmId = btmId.rename(columns={'index': 'month'})

    sizeId = sizeId.set_index(['month', 'Stkcd'])
    btmId = btmId.set_index(['month', 'Stkcd'])

    df = pd.concat([sizeId, btmId], axis=1)

    df = df.dropna(axis=0, how='any')
    df['portId'] = (df['sizeId'] * 10 + df['btmId']).astype(int)

    df = df.reset_index()

    months = sorted(df['month'].unique().tolist())
    subdfs = []
    for month in months:
        year = month.split('-')[0]
        validMonths = [year + '-0' + str(i) for i in range(7, 10)]
        validMonths += [year + '-1' + str(i) for i in range(3)]
        validMonths += [str(int(year) + 1) + '-0' + str(i) for i in range(1, 7)]

        sub = df[df['month'] == month]
        for mv in validMonths:
            tmpdf = sub.copy()
            tmpdf['month'] = mv
            subdfs.append(tmpdf)

    portId = pd.concat(subdfs, axis=0)

    portId = portId[['month', 'Stkcd', 'portId']]
    portId = portId.reset_index()
    del portId['index']
    portId.to_csv(r'D:\quantDb\researchTopics\ff5\data\portId_%s_%s.csv' % (sizeNum, btmNum))


# sizeNum,btmNum=2,3
# path=r'D:\quantDb\researchTopics\ff5\data\portId_%s_%s.csv'%(sizeNum,btmNum)
#
# df=pd.read_csv(path,index_col=0)
#
# print df.head()

def get_weight():
    df = pd.read_csv(r'D:\quantDb\researchTopics\ff5\data\MretwdAndMsmvosd.csv')
    df = df.sort_values(['Stkcd', 'Trdmnt'])
    # df=df.set_index(['Stkcd','Trdmnt'])
    subdfs=[]
    g=df.groupby('Stkcd')
    for stockId,x in list(g):
        sub=x[['Trdmnt','Msmvosd']]
        sub=sub.set_index('Trdmnt')
        sub=sub.sort_index(ascending=True)
        sub[stockId]=sub['Msmvosd'].shift(1)
        del sub['Msmvosd']
        del sub.index.name
        subdfs.append(sub)
        print stockId

    w=pd.concat(subdfs,axis=1)
    w.to_csv(r'D:\quantDb\researchTopics\ff5\data\weight.csv')


# rm0=pd.DataFrame()
# for month in df['Trdmnt'].unique().tolist():
#     sub=df[df['Trdmnt']==month]
#     sub=sub.dropna(axis=0,how='any')
#     rm0.loc[month,'rm']=mean_self(sub,'Mretwd','Msmvosd')
#     print month

# wm = lambda x: np.average(x, weights=df.loc[x.index, 'weight'])
# df = df.dropna(axis=0, how='any')
# rm = df.groupby('Trdmnt').agg({'Mretwd': wm})
# rm.columns = ['rm']
# del rm.index.name




#----------------------------------validate----------------------------------
def validate_rp():
    rp=getGTAdf('STK_MKT_FivefacMonth')
    rp=rp[rp['Portfolios']==1]

    rp=rp[rp['MarkettypeID']=='P9709']

    colnames=['TradingMonth','RiskPremium1','RiskPremium2']
    rp=rp[colnames]
    rp=rp.set_index('TradingMonth')

    myrf=pd.read_csv(r'D:\quantDb\researchTopics\ff5\data\rf.csv',index_col=0)
    myrm=pd.read_csv(r'D:\quantDb\researchTopics\ff5\data\rm.csv',index_col=0)

    myrp=(myrm['rm']-myrf['rf']).to_frame()
    myrp.columns=['myrp']

    com=pd.concat([rp,myrp],axis=1)
    com=com.dropna(axis=0,how='any')

    ax=com.cumsum().plot()
    fig=ax.get_figure()
    fig.savefig(r'D:\quantDb\researchTopics\ff5\data\validate\rp.png')







#TODO: 可扩展 ，标准格式  画图，做架构
















