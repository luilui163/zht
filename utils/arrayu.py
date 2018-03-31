# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-10  15:55
# NAME:assetPricing-arrayu.py


import numpy as np
import pandas as pd
from utils.listu import chunkify,chunkifyByBreakPoints

def _arrPortId(arr,param):
    '''
    sort the arr and divide them into n portfolio,then return the portfolio id.
    the id begin with 1,and the large the element the large the id
    :param arr:an array or list
    :param param:int or list
    :return:
    For example:
        arr=np.array(range(50))
        np.random.shuffle(arr)
        id=getPortId(arr,5)

    '''
    # arr=np.array(arr) #this line is neccessary,especially when 'arr' is a dataframe

    df = pd.DataFrame(arr)
    df.columns = ['arr']
    df = df.sort_values('arr')
    df['id'] = 0

    if isinstance(param,int):
        chunks=chunkify(range(len(arr)),param)
        idlist=[]
        for n,chunk in enumerate(chunks):
            idlist+=[n+1]*len(chunk)
        df['id']=idlist

        # for i in range(n):
        #     df['id'][int(i * len(arr)*1.0 / n):int((i + 1) * len(arr)*1.0 / n)] = i + 1  # include left but not the right

    else:#break points
        chunks=chunkifyByBreakPoints(range(len(arr)),param)
        idlist=[]
        for n,chunk in enumerate(chunks):
            idlist+=[n+1]*len(chunk)
        df['id']=idlist

        # bps = param
        # bps = np.sort(bps)
        # ns=[int(param)*len(df['id'])]
        # bvs = [0] + [int(len(arr) * bp) for bp in bps] + [len(arr)]
        # for i in range(1, len(bvs)):
        #     df['id'][bvs[i - 1]:bvs[i]] = i
    df = df.sort_index()
    return df['id'].values

def getSortedPortId(mydata,param,axis=0):
    '''

    Args:
        mydata: array,series or dataframe
        param: int or a list of break points such as [0.3,0.7]
        axis: 0 or 1,0 denotes row by row,1 means column by column,
              so,usually the index in mydata is time and the column in mydata
              is stock codes.

    Returns:

    '''
    if len(np.shape(mydata))==1:
        if isinstance(mydata,pd.DataFrame):
            ids=pd.DataFrame(index=mydata.index,columns=mydata.columns)
            tmpdf=mydata.dropna().to_frame()
            tmpdf['id']=_arrPortId(tmpdf.values,param)
            ids.loc[tmpdf.index,ids.columns[0]]=tmpdf['id'].values
            return ids

        elif isinstance(mydata,pd.Series):
            ids=pd.Series(index=mydata.index)
            tmpdf=mydata.dropna().to_frame()
            tmpdf['id']=_arrPortId(tmpdf.values,param)
            ids.loc[tmpdf.index]=tmpdf['id'].values
            return ids

        elif isinstance(mydata,np.ndarray):
            return _arrPortId(mydata,param)

    elif len(np.shape(mydata))==2:
        if isinstance(mydata,pd.DataFrame):
            ids = pd.DataFrame(columns=mydata.columns)
            for ind in mydata.index.tolist():
                sub = mydata.loc[ind].to_frame()
                sub = sub.dropna()  # this will negnect the NaN
                sub['id'] = _arrPortId(sub, param)
                ids.loc[ind] = sub['id']
            return ids


