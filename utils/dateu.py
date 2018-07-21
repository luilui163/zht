# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-10  14:44
# NAME:assetPricing-dateu.py

import datetime
import pandas as pd
from pandas.tseries.offsets import MonthEnd, Day, YearEnd
import time


def get_today():
    '''
    :return: date as string like '2018-02-01'
    '''
    today=datetime.datetime.today().strftime('%Y-%m-%d')
    return today

def get_year():
    return datetime.datetime.today().year

def get_month():
    return datetime.datetime.today().month

def get_hour():
    return datetime.datetime.today().hour


def int2Date(year,month,day):
    '''
    convert int number to date as string like
    '''
    return datetime.datetime(year,month,day).strftime('%Y-%m-%d')

def _normalize_date(date):
    '''
    :param date:str like '20180201','2018/02/01','2018/1/3'
    :return: date as string like '2018-02-01'
    '''
    if not isinstance(date,str):
        date=str(date)
    year,month,day=('','','')
    if len(date)==8:
        return '-'.join([date[:4],date[4:6],date[6:]])
    elif '-' in date:
        year,month,day=tuple(date.split('-'))
    elif r'/' in date:
        year, month, day = tuple(date.split(r'/'))
    if len(month)==1:
        month='0'+month
    if len(day) == 1:
        day = '0' + day
    return '-'.join([year, month, day])

def normalize_date(dates):
    '''
    :param dates:type as the input parameter in _normalize_date() or a list of
        element as this type.
    :return: str if 'dates' is a str or int else list
    '''
    if isinstance(dates,(str,int)):
        return _normalize_date(dates)
    else:
        return [_normalize_date(date) for date in dates]

def freq_end(x, freq):
    '''
    convert the date format,this funnction is useful,especially for dataframe

    :param x:array-like,usually it can be df.index
    :param freq: offsets from pandas.tseries.offsets,such as 'Y','M','D'
    :return:calendar end of month,year or day.
    '''
    if freq=='Y':
        #for freq=='Y',the element in x must be like 1995.
        x=pd.to_datetime(x,format='%Y')+YearEnd(0)
    elif freq=='M':
        x=pd.to_datetime(x)+MonthEnd(0)
    elif freq=='D': #TODO: test with freq=='D'
        x=pd.to_datetime(x)+Day(0)
        #for freq=='Y',the element in x must be like 1995.
    return x

def get_current_time(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format)
