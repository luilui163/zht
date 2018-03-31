#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import time

def normalize_date_format(date):
    '''
    d1='2013/2/7'
    d2='2013-2-7'
    return:'20161111'
    '''
    if '/' in date:
        year,month,day=date.split(r'/')
        month=month if len(month)==2 else '0'+month
        day=day if len(day)==2 else '0'+day
        new_date=year+month+day
        return new_date
    elif '-' in date:
        year,month,day=date.split(r'-')
        month=month if len(month)==2 else '0'+month
        day=day if len(day)==2 else '0'+day
        new_date=year+month+day
        return new_date
    else:
        return date

def str_to_datetime(dates):
    '''
    deal with a single str or a list of str
    '''
    if type(dates)==list:
        dates = [normalize_date_format(date) for date in dates]
        new_dates1=[d[:4]+'-'+d[4:6]+'-'+d[6:] for d in dates]
        new_dates2=[pd.Timestamp(nd) for nd in new_dates1]
        return new_dates2
    elif type(dates)==str:
        new_date1=dates[:4]+'-'+dates[4:6]+'-'+dates[6:]
        return pd.Timestamp(new_date1)



def get_tradedates():
    end_date=time.strftime('%Y%m%d',time.localtime(time.time()))
    start_date='20090101'

    tradedates=c.tradedates(start_date,end_date).Data
    with open('tradedates.txt','w') as f:
        for td in tradedates:
            f.write(normalize_date_format(td)+'\n')
