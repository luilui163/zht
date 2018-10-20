# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-08-21  15:38
# NAME:FT_hp-update_financial_data.py

import multiprocessing
import pickle

import datetime
from itertools import chain, islice

from WindPy import w
import numpy as np
import pandas as pd
import os

DIR=r'E:\wind'

w.start()

DATE_FORMAT='%Y-%m-%d'

def test_wind():
    print(w.isconnected())
    data=w.wss("000001.SZ,000002.SZ,000004.SZ,000005.SZ", "trade_code")
    return

def wrapper_log(func):
    def wrapper(*args,**kwargs):
        print('start---->',func.__name__)
        return func(*args,**kwargs)
    return wrapper

def chunks(iterable, size=500):
    '''chunks an iterable into n smaller generator with the given maximium size for each generator,
    The function will keep the initial order.

    refer to https://stackoverflow.com/questions/24527006/split-a-generator-into-chunks-without-pre-walking-it
    '''
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))

def _multi_p(func,args_iter,n,multi_parameters):
    '''
        make sure that all the data needed by "func" should be sent by parameters, try to avoid calling
        the data outside the "func" since sometimes the processes may be frozen without raising any
        error.

        Args:
            func:
            args_iter:
            n:
            multi_parameters:

        Returns:

        '''
    pool = multiprocessing.Pool(n)
    if multi_parameters:
        results = pool.starmap(func, args_iter)
    else:
        results = pool.map(func, args_iter)
    pool.close()  # trick: close the processing every time the pool has finished its task, and pool.close() must be called before pool.join()
    pool.join()
    # refer to https://stackoverflow.com/questions/38271547/when-should-we-call-multiprocessing-pool-join
    return results

def multi_process(func, args_iter, n=15, multi_parameters=False, size_in_each_group=None):
    '''

    Args:
        func:
        args_iter:
        n:
        multi_parameters:
        size_in_each_group:None or int, the times of the task being called in each _multi_p function,
        by default it is None. This parameters can be set in case "_multi_p" will consume more and
        more memory when the 'task' is called over and over again. With 'size_in_each_group" set
        '_multi_p' will be ended and start again each time it has finished the given number of task to save momery.


    Returns:

    '''
    if size_in_each_group is None:
        return _multi_p(func, args_iter, n, multi_parameters)
    else:
        rs=[]
        for sub_args_iter in chunks(args_iter, size_in_each_group):
            rs+=_multi_p(func,sub_args_iter,n,multi_parameters)
        return rs

def get_today(format=DATE_FORMAT):
    '''
    :return: date as string like '2018-02-01'
    '''
    today=datetime.datetime.today().strftime(format)
    return today

def get_stkcd_list(date=None):
    if date is None:
        date=get_today(DATE_FORMAT)
    path=os.path.join(DIR,'stkcd_list',f'{date}.pkl')
    if os.path.exists(path):
        return pickle.load(open(path,'rb'))
    else:
        codes=w.wset("SectorConstituent",u"date={};sector=全部A股".format(date)).Data[1]
        f=open(path,'wb')
        pickle.dump(codes,f)
        return codes

def get_ann_dt_df(date):
    path=os.path.join(DIR,'ann_dt',f'{date}.pkl')
    if os.path.exists(path):
        return pd.read_pickle(path)
    else:
        # codes = get_today_stkcd_list()
        codes=get_stkcd_list(date)
        result = w.wsd(','.join(codes), "stm_issuingdate", "ED-2Q", date,
                       "Period=Q;Days=Alldays")
        if result.ErrorCode is not 0:
            raise ValueError
        ann_dt = pd.DataFrame(result.Data, index=result.Codes,
                              columns=result.Times).T
        ann_dt.to_pickle(path)
        return ann_dt

def get_latest(date,prefix,suffix='pkl'):
    '''
    get the latest cache before "date"
    Args:
        date:
        prefix:str,{'ann_dt','stkcd_list'}

    Returns:

    '''
    anns=[an for an in os.listdir(os.path.join(DIR,prefix)) if pd.to_datetime(an[:-4])<pd.to_datetime(date)]
    anns = sorted(anns, key=lambda x: pd.to_datetime(x[:-4]))
    if suffix=='pkl':
        return pickle.load(open(os.path.join(DIR,prefix,anns[-1]),'rb'))
    elif suffix=='csv':
        return pd.read_csv(os.path.join(DIR,prefix,anns[-1]),index_col=0)


def get_data_for_one_stk(stkcd, rpdate, indicators):
    path=os.path.join(DIR,'financial_cache',f'{rpdate}_{stkcd}.csv') #trick: do not use .pkl,sometimes it may be malformed
    if os.path.exists(path):
        s=pd.read_csv(path,index_col=0,parse_dates=True)
    else:
        data = w.wsd(stkcd, ','.join(indicators), rpdate, rpdate, "unit=1;rptType=1;Period=Q;Days=Alldays")
        if data.ErrorCode is not 0:
            raise ValueError
        s = pd.Series([d[0] for d in data.Data], index=indicators)
        s.fillna(value=np.nan, inplace=True)
        print('Getting data for {}-----{}'.format(rpdate,stkcd))
        s.to_csv(path)#trick: cache
    return s

def get_target_df(date):
    '''
        get the df to be updated at the given date
    Returns:DataFrame, index is report period and the columns is stock codes, the
        value is the announcement date.

    Args:
        date:

    Returns:

    '''
    # if date is None:
    #     date=get_today()
    new_ann_dt=get_ann_dt_df(date)
    old_ann_dt=get_latest(date,'ann_dt')

    new_index=new_ann_dt.index.union(old_ann_dt.index)
    new_column=new_ann_dt.columns.union(old_ann_dt.columns)

    new_ann_dt=new_ann_dt.reindex(index=new_index,columns=new_column)
    old_ann_dt=old_ann_dt.reindex(index=new_index,columns=new_column)

    target_df=new_ann_dt[new_ann_dt!=old_ann_dt]
    return target_df


def fetch_data(target_df):
    '''
    get data fromm wind
    Args:
        target_df: DataFrame,

    Returns:DataFrame

    '''
    name_df = pd.read_excel(os.path.join(DIR,'indicators_name.xlsx'), sheet_name='financial')
    dfs = []
    for date, row in target_df.iterrows():
        row = row.dropna()
        if len(row)>0:
            row = row.apply(lambda x: x.strftime(DATE_FORMAT))
            rpdate = row.name.strftime(DATE_FORMAT)
            stkcds = row.index.tolist()
            indicators = name_df['wind_name'].tolist()
            _df = pd.concat([get_data_for_one_stk(stkcd, rpdate, indicators) for stkcd in stkcds], axis=1,sort=True).T
            _df['rpdate'] = rpdate
            _df.set_index('rpdate', append=True, inplace=True)
            _df.index.names = ['stkcd', 'rpdate']
            _df=_df.swaplevel()
            dfs.append(_df)
    df = pd.concat(dfs,sort=True)

    return df

def _read_financial_cache(fn):
    s=pd.read_csv(os.path.join(DIR,'financial_cache',fn),index_col=0,parse_dates=True,header=None).iloc[:,0]
    return s


def combine_cache(date):
    fns=os.listdir(os.path.join(DIR,'financial_cache'))
    ss=multi_process(_read_financial_cache, fns, n=30)
    keys=((fn.split('_')[0],fn.split('_')[1][:-4]) for fn in fns)

    comb=pd.concat(ss,axis=1,keys=keys,sort=True).T
    comb.index.names=['rpdate','stkcd']
    comb=comb.reset_index()
    comb['rpdate']=pd.to_datetime(comb['rpdate'])
    comb=comb.set_index(['rpdate','stkcd']).sort_index()
    comb=comb.dropna(how='all',axis=1)
    comb['stm_issuingdate']=pd.to_datetime(comb['stm_issuingdate'])
    comb=comb[comb['stm_issuingdate']<=date] #trick:
    return comb

@wrapper_log
def update_consensus(date):
    path=os.path.join(DIR,'consensus',f'{date}.csv')
    if os.path.exists(path):
        return

    indicators=["west_netprofit_FY1",
                "west_netprofit_FY2",
                "west_netprofit_FY3",
                "west_sales_FY1",
                "west_sales_FY2",
                "west_sales_FY3",
                "west_avgbps_FY1",
                "west_avgbps_FY2",
                "west_avgbps_FY3",
                ]
    codes = get_stkcd_list(date)
    data=w.wss(','.join(codes),','.join(indicators),f'unit=1;tradeDate={date}')
    if data.ErrorCode is not 0:
        raise ValueError
    predicted=pd.DataFrame(data.Data,index=data.Fields,columns=data.Codes)

    # update baseshare
    y=date[:4]
    years=[str(int(y)+i) for i in range(3)]
    ss=[]
    for i,year in enumerate(years):
        data=w.wss(codes, "west_avgshares",f"unit=1;tradeDate={date};year={year};westPeriod=180")
        if data.ErrorCode is not 0:
            raise ValueError
        s=pd.Series(data.Data[0],index=data.Codes,name=f'baseshare_FY{i+1}')
        ss.append(s)
    baseshare=pd.concat(ss,axis=1).T

    df=pd.concat([predicted,baseshare],axis=0).T
    df.to_csv(path)

@wrapper_log
def update_financial(date):
    path=os.path.join(DIR,'financial',f'{date}.csv')
    if os.path.exists(path):
        return

    target_df=get_target_df(date) #fixme:
    if target_df.notnull().sum().sum()>0:
        fetch_data(target_df)

    df=combine_cache(date)
    # df.to_pickle(os.path.join(DIR,'financial',f'{date}.pkl'))
    df.to_csv(path)

@wrapper_log
def update_fundamental(date):
    path=os.path.join(DIR,'fundamental',f'{date}.csv')
    if os.path.exists(path):
        return
    codes = get_stkcd_list(date) #fixme:
    indicators=['total_shares','float_a_shares','share_totala','mkt_freeshares','dividendyield2']
    data=w.wss(','.join(codes),','.join(indicators),f'unit=1;tradeDate={date}')
    if data.ErrorCode is not 0:
        raise ValueError
    df = pd.DataFrame(data.Data, index=data.Fields, columns=data.Codes).T
    df.to_csv(path)

@wrapper_log
def update_ipodate(date):
    path=os.path.join(DIR,'ipo_date',f'{date}.csv')
    if os.path.exists(path):
        return

    old_codes=get_latest(date,'stkcd_list')
    all_codes=get_stkcd_list(date)
    new_codes=[c for c in all_codes if c not in old_codes]
    if len(new_codes)>0:
        #TODO: new_code is a single str
        ipodata=w.wss(','.join(new_codes), "ipo_date")
        if ipodata.ErrorCode is not 0:
            raise ValueError
        increment=pd.DataFrame(ipodata.Data[0],index=ipodata.Codes,columns=['ipo_date'])
        old_data=get_latest(date,'ipo_date','csv')
        new=pd.concat([old_data,increment],axis=0).sort_index()
    else:
        new=get_latest(date,'ipo_date','csv')
    new.to_csv(path)


def get_test_dates_list():
    directory=os.path.join(DIR,'stkcd_list')
    fns=os.listdir(directory)
    dates=[fn[:-4] for fn in fns]
    dates=sorted(dates,key=lambda x:pd.to_datetime(x))
    return dates

def update_single_date(date=None):
    if date is None:
        date=get_today()

    update_ipodate(date)
    update_financial(date)
    update_consensus(date)
    update_fundamental(date)


def update_periods(start,end=None):
    if end is None:
        end=get_today()
    dates=pd.date_range(start=start,end=end,freq='D')
    dates=[d.strftime(DATE_FORMAT) for d in dates]
    for date in dates:
        update_single_date(date)
        print(date)

def debug():
    dates=pd.date_range(start='2018-08-30',end=get_today(),freq='D')
    dates=[d.strftime(DATE_FORMAT) for d in dates]
    for date in dates:
        print(f'Updating data for ------>{date}')
        update_single_date(date)

def debug1():
    dates=get_test_dates_list()[14:]

    for date in dates:
        update_financial(date)
        print(date)

if __name__ == '__main__':
    update_periods(start='2018-09-01')









#TODO: logger and multiprocessing
#TODO: change the indictor names
#TODO: only update in trading date





