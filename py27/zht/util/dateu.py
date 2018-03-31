#-*-coding: utf-8 -*-
#@author:tyhj
import datetime
import os

def getToday():
    '''
    :return:'yyyy-MM-DD'
    '''
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    return today

def int2Date(year,month,day):
    '''
    :param year:
    :param month:
    :param day:
    :return: 'YYYY-MM-DD'
    '''
    return datetime.datetime(year,month,day).strftime('%Y-%m-%d')


#获的日期的交集
def get_date_intersection(directory):
    '''
    :param directory: the target directory in which there are several
    subdirectorys
    :return: the date_intersection in these subdirectory,in list type
    '''
    factor_names=os.listdir(directory)

    date_intersection=[]
    for i,fn in enumerate(factor_names):
        file_names=os.listdir(os.path.join(directory,fn))
        dates=[fn[:10] for fn in file_names]
        if i == 0:
            date_intersection=dates
        else:
            date_intersection=[d for d in date_intersection if d in dates]
    return date_intersection


def _normalize_date(date):
    date=str(date)
    year,month,day=('','','')
    if len(date)==8:
        return '-'.join(date[:4],date[4:6],date[6:])
    elif '-' in date:
        year,month,day=tuple(date.split('-'))
    elif r'/' in date:
        year, month, day = tuple(date.split(r'/'))
    if len(month)==1:
        month='0'+month
    if len(day) == 1:
        day = '0' + day
    return '-'.join([year, month, day])


# def _normalize_date(date):
#     '''
#     normalize date with form in '2016-03-09' or '2012/3/6'
#     '''
#     try:
#         int(date)
#         return date
#     except:
#         print date
#         if '-' in date:
#             year, month, day = tuple(date.split('-'))
#         elif r'/' in date:
#             year, month, day = tuple(date.split(r'/'))
#
#         if len(month) == 1:
#             month = '0' + month
#         if len(day) == 1:
#             day = '0' + day
#         return '-'.join([year,month,day])

def normalize_date(dates):
    if isinstance(dates,str):
        return _normalize_date(dates)
    else:
        newDates=[]
        for date in dates:
            newDates.append(_normalize_date(date))
        return newDates

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


def today():
    day = datetime.datetime.today().date()
    return str(day)


def get_year():
    year = datetime.datetime.today().year
    return year


def get_month():
    month = datetime.datetime.today().month
    return month


def get_hour():
    return datetime.datetime.today().hour


def today_last_year():
    lasty = datetime.datetime.today().date() + datetime.timedelta(-365)
    return str(lasty)


def day_last_week(days = -7):
    lasty = datetime.datetime.today().date() + datetime.timedelta(days)
    return str(lasty)


def get_now():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def int2time(timestamp):
    datearr = datetime.datetime.utcfromtimestamp(timestamp)
    timestr = datearr.strftime("%Y-%m-%d %H:%M:%S")
    return timestr


def diff_day(start = None, end = None):
    d1 = datetime.datetime.strptime(end, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(start, '%Y-%m-%d')
    delta = d1 - d2
    return delta.days


def get_quarts(start, end):
    idx = pd.period_range('Q'.join(year_qua(start)), 'Q'.join(year_qua(end)),
                          freq = 'Q-JAN')
    return [str(d).split('Q') for d in idx][::-1]


