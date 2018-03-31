#-*-coding: utf-8 -*-
#author:tyhj
#getData.py 2017/9/18 17:19

import pandas as pd
from shutil import copyfile

from zht.util.dfFilter import filterDf
from zht.util.pandasu import get_inter_frame
from zht.data.gta import gtaApi
from zht.util.pandasu import flatten2panel

from params import *

def _readFromTmp(fn):
    df=pd.read_csv(os.path.join(tmpp,fn+'.csv'),index_col=0)
    return df

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
    nf.to_csv(os.path.join(tmpp,'nfc.csv'))

# get_nfc()

def get_items1():
    # 涉及report的表
    def _get_indicator1(name, tbname, fldname, timefld='Accper'):
        df = pd.read_csv(os.path.join(sp, tbname + '.csv'))
        df = df[df['Typrep'] == 'A']
        q = 'Accper endswith 12-31'
        df = filterDf(df, q)
        colnames = ['Stkcd', timefld, fldname]
        df = df[colnames]
        subdfs = []
        for stockId, x in list(df.groupby('Stkcd')):
            tmpdf = x[[timefld, fldname]]
            tmpdf = tmpdf.set_index(timefld)
            tmpdf.index = [ind[:-3] for ind in tmpdf.index]
            tmpdf.columns = [stockId]
            subdfs.append(tmpdf)

        table = pd.concat(subdfs, axis=1)
        table = table.sort_index(ascending=True)
        table.to_csv(os.path.join(tmpp, name + '.csv'))

    items=[('operIncom','FS_Comins','B001101000','Accper'),
            ('operExp','FS_Comins','B001209000','Accper'),
            ('admExp','FS_Comins','B001210000','Accper'),
            ('finanExp','FS_Comins','B001211000','Accper'),
            ('totAsset','FS_Combas','A001000000','Accper'),
            ('totShe','FS_Combas','A003000000','Accper')
           ]
    for item in items:
        name,tbname,fldname,timefld=item
        _get_indicator1(name,tbname,fldname,timefld)
        print name

# get_items1()

def get_op():
    '''
    Returns:

    '''
    operIncom=_readFromTmp('operIncom')
    admExp=_readFromTmp('admExp').fillna(method='ffill')
    finanExp=_readFromTmp('finanExp').fillna(method='ffill')
    operExp=_readFromTmp('operExp').fillna(method='ffill')

    op=operIncom-admExp-finanExp-operExp
    op.index=[str(int(ind[:4])+1)+'-06' for ind in op.index] #TODO:In june of year t,op comes from fiscal year ending in year t-1
    op.to_csv(os.path.join(tmpp,'op.csv'))#the data is up to date(current available data)

# get_op()

def get_inv():
    totAsset=_readFromTmp('totAsset')
    inv=totAsset.pct_change()
    inv.index = [str(int(ind[:4]) + 1) + '-06' for ind in inv.index]#TODO:In june of year t,inv comes from fiscal year ending in year t-1
    inv.to_csv(os.path.join(tmpp,'inv.csv'))#the data is up to date(current available data)

# get_inv()

def get_items2():
    # 涉及 trading 数据的表
    def _get_indicator2(name, tbname, fldname, timefld='Trdmnt'):
        df = pd.read_csv(os.path.join(sp, tbname + '.csv'))
        q = 'Markettype in [1,4,16]'
        df = filterDf(df, q)
        colnames = ['Stkcd', timefld, fldname]

        df = df[colnames]
        subdfs = []
        for stockId, x in list(df.groupby('Stkcd')):
            tmpdf = x[[timefld, fldname]]
            tmpdf = tmpdf.set_index(timefld)
            tmpdf.columns = [stockId]
            subdfs.append(tmpdf)

        table = pd.concat(subdfs, axis=1)
        table = table.sort_index(ascending=True)
        table.to_csv(os.path.join(tmpp, name + '.csv'))

    items=[
        ('ret','TRD_Mnth','Mretwd','Trdmnt'),
        ('size','TRD_Mnth','Msmvosd','Trdmnt'),

    ]
    for item in items:
        name,tbname,fldname,timefld=item
        _get_indicator2(name,tbname,fldname,timefld)
        print name

# get_items2()

def get_weight():
    size=_readFromTmp('size')
    weight=size.shift(1)# the weight is the size at the end of the last month
    weight.to_csv(os.path.join(tmpp,'weight.csv'))

# get_weight()

def get_rf():
    df = pd.read_csv(os.path.join(sp,'TRD_Nrrate.csv'))
    q = 'Nrr1 == NRI01'  # TODO:TBC=国债票面利率
    df = filterDf(df, q)
    colnames = ['Clsdt', 'Nrrmtdt']
    df = df.sort_values('Clsdt')

    df = df[colnames]
    df = df.set_index('Clsdt')

    dates = pd.date_range(df.index[0], df.index[-1], freq='D')
    dates = [d.strftime('%Y-%m-%d') for d in dates]

    newdf = pd.DataFrame(index=dates)
    newdf['Nrrmtdt'] = df['Nrrmtdt']
    newdf = newdf.fillna(method='ffill')
    newdf = newdf.reset_index()
    newdf['month'] = newdf['index'].apply(lambda x: '-'.join(x.split('-')[:-1]))

    avg = newdf.groupby('month').mean()
    avg = avg / 100
    del avg.index.name
    avg.columns = ['rf']
    avg.to_csv(os.path.join(tmpp,'rf.csv'))

# get_rf()

def get_rm():
    '''
    monthly market return
    Returns:

    '''
    name='rm'
    dbname=''
    tbname='TRD_Cnmont'
    fldname='Cmretwdos'
    timefld='Trdmnt'
    q=[]
    cols=[]

    df = pd.read_csv(os.path.join(sp, tbname + '.csv'))
    q = 'Markettype == 5'#综合A股市场
    df = filterDf(df, q)
    colnames = [timefld, fldname]

    df = df[colnames]

    df=df.set_index('Trdmnt')
    df=df.sort_index()
    del df.index.name
    df.columns=['rm']
    df.to_csv(os.path.join(tmpp,'rm.csv'))

# get_rm()

def get_rp():
    '''
    premium market return,rm-rf
    Returns:

    '''
    rf=_readFromTmp('rf')
    rm=_readFromTmp('rm')

    rp=rm['rm']-rf['rf']

    rp=rp.to_frame()
    rp.columns=['rp']
    rp.to_csv(os.path.join(tmpp,'rp.csv'))

# get_rp()

def get_mv():
    '''
    market value of per share
    Returns:

    '''
    name='mv'
    tbname='TRD_Mnth'
    fldname='Mclsprc' #月收盘价
    timefld='Trdmnt'

    df = pd.read_csv(os.path.join(sp, tbname + '.csv'))
    q1 = 'Markettype in [1,4,16]'
    q2= 'Trdmnt endswith 12' #TODO: only need the data in December
    q=[q1,q2]
    df = filterDf(df, q)
    colnames = ['Stkcd', timefld, fldname]

    df = df[colnames]
    subdfs = []
    for stockId, x in list(df.groupby('Stkcd')):
        tmpdf = x[[timefld, fldname]]
        tmpdf = tmpdf.set_index(timefld)
        tmpdf.columns = [stockId]
        subdfs.append(tmpdf)

    table = pd.concat(subdfs, axis=1)
    table = table.sort_index(ascending=True)
    table.to_csv(os.path.join(tmpp,name+'.csv'))

# get_mv()

def get_bv():
    '''
    book value of per share
    Returns:

    '''
    name='bv'
    tbname='FI_T9'
    fldname='F091001A' #每股净资产
    timefld='Accper'

    df = pd.read_csv(os.path.join(sp, tbname + '.csv'))

    q1 = 'Typrep == A'
    q2 = 'Accper endswith 12-31'  # TODO: only need annual report
    q = [q1, q2]
    df = filterDf(df, q)
    colnames = ['Stkcd', timefld, fldname]

    df = df[colnames]
    subdfs = []
    for stockId, x in list(df.groupby('Stkcd')):
        tmpdf = x[[timefld, fldname]]
        tmpdf = tmpdf.set_index(timefld)
        tmpdf.columns = [stockId]
        subdfs.append(tmpdf)

    table = pd.concat(subdfs, axis=1)
    # do not adjust for the time-lag,this will be done in the process of calculing btm
    table.index=[ind[:-3] for ind in table.index]
    table = table.sort_index(ascending=True)
    table.to_csv(os.path.join(tmpp,name+'.csv'))

# get_bv()

def get_btm():
    '''
    book to market ratio
    Returns:

    '''
    bv=_readFromTmp('bv')
    mv=_readFromTmp('mv')

    bv,mv=get_inter_frame([bv,mv])
    btm=bv/mv
    btm.index = [str(int(ind[:4]) + 1) + '-06' for ind in btm.index]
    btm.to_csv(os.path.join(tmpp,'btm.csv'))

# get_btm()

def get_eret():
    '''
    monthly,stock excess ret

    Returns:

    '''
    ret = pd.read_csv(os.path.join(tmpp, 'ret.csv'), index_col=0)
    rf = pd.read_csv(os.path.join(tmpp, 'rf.csv'), index_col=0)
    eret = ret.sub(rf['rf'], axis=0)
    eret.to_csv(os.path.join(tmpp,'eret.csv'))

# get_eret()

def moveFiles():
    bdpFiles=['ret','weight','rf','rp','nfc','eret']
    idpFiles=['btm','inv','op']

    for bdpf in bdpFiles:
        src=os.path.join(tmpp,bdpf+'.csv')
        dst=os.path.join(bdp,bdpf+'.csv')
        if not os.path.exists(dst):
            copyfile(src,dst)

    for idpf in idpFiles:
        src=os.path.join(tmpp,idpf+'.csv')
        dst=os.path.join(idp,idpf+'.csv')
        if not os.path.exists(dst):
            copyfile(src,dst)

    size=pd.read_csv(os.path.join(tmpp,'size.csv'),index_col=0)
    newInd=[ind for ind in size.index if ind.endswith('06')]
    size=size.reindex(index=newInd)
    size.to_csv(os.path.join(idp,'size.csv'))

# moveFiles()


#======================
def getFinancialRatio():
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
        namedict={tmpdf['Fldname'].values[i]:tmpdf['Title'].values[i] for i in range(tmpdf.shape[0])}
        for variable in variables:
            indvar='Accper'
            colvar='Stkcd'
            vname=variable
            indicator=flatten2panel(df,indvar,colvar,vname)

            newIndex=[ind for ind in indicator.index if ind.endswith('12-31')]
            indicator=indicator.reindex(index=newIndex)
            indicator.index=[str(int(ind[:4])+1)+'-06' for ind in indicator.index]
            indicator.to_csv(os.path.join(idp,namedict[vname]+'.csv'))

            print tbname,vname

#TODO:delete those indicators with too short history window

# getIndicatorsFromReport()

# def getFinancialIndicatorsFromReport():
#     tbnames=['FS_Comins','FS_Comscfi','FS_Comscfd','FS_Combas']
#     for tbname in tbnames:
#         q='Typrep == A'
#
#         namedf=pd.read_csv(os.path.join(r'D:\quantDb\sourceData\gta\data\tablesNew',tbname+'.csv'),index_col=0)
#         namedict={namedf['Fldname'].values[i]:namedf['Title'].values[i] for i in range(namedf.shape[0])}
#
#         unvar=['Accper','Stkcd','Typrep']
#         indvar='Accper'
#         colvar='Stkcd'
#
#         df=gtaApi.readFromSrc(tbname)
#         df=filterDf(df,q)
#         for vname in df.columns:
#             if vname not in unvar:
#                 indicator=flatten2panel(df,indvar,colvar,vname)
#
#                 newIndex = [ind for ind in indicator.index if ind.endswith('12-31')]
#                 indicator = indicator.reindex(index=newIndex)
#                 indicator.index = [str(int(ind[:4]) + 1) + '-06' for ind in indicator.index]
#                 indicator.to_csv(os.path.join(idp, namedict[vname] + '.csv'))
#             # print tbname,vname





#TODO: calculate those famous anomalies in classical papers








# if __name__=='__main__':
#     get_nfc()
#     get_items1()
#     get_items2()
#     get_op()
#     get_inv()
#     get_items2()
#     get_weight()
#     get_rf()
#     get_rm()
#     get_rp()
#     get_mv()
#     get_bv()
#     get_btm()
#     get_eret()
#     moveFiles()
#     getIndicatorsFromReport()