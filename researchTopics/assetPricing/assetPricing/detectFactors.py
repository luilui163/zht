#-*-coding: utf-8 -*-
#author:tyhj
#detectFactors.py 2017/9/3 9:13

import pandas as pd
import os

from params import idp
from params import zhang
import params
from zht.data.gta import gtaApi
from zht.util.dfFilter import filterDf
from zht.util.pandasu import flatten2panel,getSortedId


#get raw indicators

def getRawIndicators():
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
            mydf.to_csv(os.path.join(params.rawIndicatorPath,adict[vname]+'.csv'))
            print tbname,vname


fns=os.listdir(params.rawIndicatorPath)
fn=fns[0]
df=pd.read_csv(os.path.join(params.rawIndicatorPath,fn),index_col=0)
dfid=getSortedId(df,10)
print dfid














