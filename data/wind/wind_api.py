# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-08-15  16:04
# NAME:zht-wind_api.py
import datetime
import pickle

from WindPy import w
from utils.dateu import get_today

DIR=r'e:\tmp_wind'

w.start()

import pandas as pd
import os

DATE_FORMAT='%Y-%m-%d'

df=pd.read_excel(r'C:\Users\zht\Desktop\indicators_name.xlsx',sheet_name='financial')


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
        result=w.wsd(','.join(codes), "stm_issuingdate", "ED-2Q", get_today(), "Period=Q;Days=Alldays")
        ann_dt=pd.DataFrame(result.Data,index=result.Codes,columns=result.Times).T
        f=open(path,'wb')
        pickle.dump(ann_dt,f)
        return ann_dt

ann_dt=get_ann_dt()

ann_dt.index=map(lambda x:x.strftime(DATE_FORMAT),ann_dt.index)

ann_dt=ann_dt.applymap(lambda x:x.strftime(DATE_FORMAT) if not isinstance(x,pd._libs.tslibs.nattype.NaTType) else x)
# test=ann_dt[ann_dt==get_today()]
# test=test.dropna(how='all',axis=0).dropna(how='all',axis=1)

for date,row in ann_dt.iterrows():
    print(date,row[row==get_today(DATE_FORMAT)]) #fixme: <= rather than ==

row=ann_dt.iloc[-2,:]
row=row[row==get_today(DATE_FORMAT)]

rpdate=row.name

stkcds=row.index.tolist()
indicators=df['wind_name'].tolist()


stkcd=stkcds[0]

test=w.wsd(stkcd, ','.join(indicators), rpdate,rpdate, "unit=1;rptType=1;Period=Q;Days=Alldays")









#TODO: 合并报表
