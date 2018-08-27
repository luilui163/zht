# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-08-15  16:04
# NAME:zht-wind_api.py
import datetime
import multiprocessing
import pickle

from WindPy import w
from utils.dateu import get_today
import numpy as np


DIR=r'e:\tmp_wind'

w.start()

import pandas as pd
import os

DATE_FORMAT='%Y-%m-%d'

def multi_task(func, args_iter, n=8):
    pool=multiprocessing.Pool(n)
    results=pool.map(func, args_iter)
    pool.close()#trick: close the processing every time the pool has finished its task, and pool.close() must be called before pool.join()
    pool.join()
    #refer to https://stackoverflow.com/questions/38271547/when-should-we-call-multiprocessing-pool-join
    return results

def get_stkcd_list():
    today = get_today(DATE_FORMAT)
    path=os.path.join(DIR,'stkcd_list_{}.pkl'.format(today))
    if os.path.exists(path):
        return pickle.load(open(path,'rb'))
    else:
        codes=w.wset("SectorConstituent",u"date={};sector=全部A股".format(today)).Data[1]
        f=open(path,'wb')
        pickle.dump(codes,f)
        return codes

def get_ann_dt():
    today=get_today(DATE_FORMAT)
    path=os.path.join(DIR,'ann_dt_{}.pkl'.format(today))
    if os.path.exists(path):
        return pickle.load(open(path,'rb'))
    else:
        codes=get_stkcd_list()
        result=w.wsd(','.join(codes), "stm_issuingdate", "ED-5Q", get_today(), "Period=Q;Days=Alldays")
        ann_dt=pd.DataFrame(result.Data,index=result.Codes,columns=result.Times).T
        f=open(path,'wb')
        pickle.dump(ann_dt,f)
        return ann_dt

def get_last_ann_dt():
    anns=[an for an in os.listdir(os.path.join(DIR)) if an.startswith('ann_dt') and an[7:-4] !=get_today()]
    anns=sorted(anns,key=lambda x:pd.to_datetime(x[7:-4]))
    return pd.read_pickle(os.path.join(DIR,anns[-1]))

def get_data_for_one_stk(args):
    stkcd, rpdate, indicators=args
    data = w.wsd(stkcd, ','.join(indicators), rpdate, rpdate, "unit=1;rptType=1;Period=Q;Days=Alldays").Data
    s = pd.Series([d[0] for d in data], index=indicators)
    s.fillna(value=np.nan, inplace=True)
    s.name=stkcd
    print('Getting data for {}-----{}'.format(rpdate,stkcd))
    return s

def get_new_df():
    ann_dt=get_ann_dt()
    last_ann_dt=get_last_ann_dt()

    new_index=ann_dt.index.union(last_ann_dt.index)
    new_column=ann_dt.columns.union(last_ann_dt.columns)

    ann_dt=ann_dt.reindex(index=new_index,columns=new_column)
    last_ann_dt=last_ann_dt.reindex(index=new_index,columns=new_column)
    new_df=ann_dt[ann_dt!=last_ann_dt]
    return new_df

def get_new_data(ann_dt_df):
    name_df = pd.read_excel(os.path.join(DIR,r'indicators_name.xlsx'), sheet_name='financial')
    dfs = []
    for date, row in ann_dt_df.iterrows():
        row = row.dropna()
        row = row.apply(lambda x: x.strftime(DATE_FORMAT))
        rpdate = row.name.strftime(DATE_FORMAT)
        stkcds = row.index.tolist()
        indicators = name_df['wind_name'].tolist()
        # _df=pd.concat(multi_task(get_data_for_one_stk,((stkcd, rpdate, indicators) for stkcd in stkcds)),axis=1).T
        _df = pd.concat([get_data_for_one_stk((stkcd, rpdate, indicators)) for stkcd in stkcds], axis=1).T
        _df['rpdate'] = rpdate
        _df.set_index('rpdate', append=True, inplace=True)
        _df.index.names = ['stkcd', 'rpdate']
        # df.to_pickle(os.path.join(DIR,'data_{}.pkl'.format(get_today())))
        dfs.append(_df)
    df = pd.concat(dfs)
    return df

# today_updated.to_pickle(os.path.join(DIR, 'today_updated_{}.pkl'.format(get_today())))


#TODO: how to combine the old and the new dataframe


# codes = get_stkcd_list()
# result = w.wsd(','.join(codes), "stm_issuingdate", "ED-5Q", get_today(), "Period=Q;Days=Alldays")
# ann_dt = pd.DataFrame(result.Data, index=result.Codes, columns=result.Times).T
#
# ann_dt.to_pickle(os.path.join(DIR,'ann_dt_{}.pkl'.format(get_today())))
#
# test_ann_dt=ann_dt.iloc[:,30]
#
# df=get_new_data(ann_dt)

def test():
    ann_dt=pd.read_pickle(os.path.join(DIR,'ann_dt_{}.pkl'.format(get_today())))
    test_ann_dt=ann_dt.iloc[:,:30]
    df=get_new_data(test_ann_dt)
    df.to_pickle('test_df.pkl')

if __name__ == '__main__':
    test()



#TODO: logger and multiprocessing

