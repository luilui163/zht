#-*-coding: utf-8 -*-
#@author:tyhj


def _extractDate1(dateStr):
    '''
    extract date from a str
    :param dateStr: str
    :return: date,format like '2010-02-04'
    '''
    if len(dateStr)==10 and dateStr.count('-')==2:
        return dateStr
    elif len(dateStr)==10 and dateStr.count(r'/')==2:
        return dateStr.replace(r'/','-')
    elif len(dateStr) == 8 and dateStr.isdigit():
        return dateStr[:4] + '-' + dateStr[4:6] + dateStr[6:]
    else:
        raise TypeError('the format of dateStr is wrong!')

def _extractDate(dateStr):
    if r'/' in dateStr:
        year,month,day=dateStr.split(r'/')
        month='0'*(2-len(month))+month
        day='0'*(2-len(day))+day
        return r'-'.join([year,month,day])
    elif len(dateStr)==8 and dateStr.isdigit():
        return dateStr[:4] + '-' + dateStr[4:6] + dateStr[6:]
    else:
        raise TypeError('the format of dateStr is wrong!')

def extractDate(s):
    if isinstance(s,str):
        return _extractDate(s)
    else:
        news=[]
        for ss in s:
            news.append(_extractDate(ss))
        return news




def normalize_sid(sid):
    sid=sid.upper()
    return sid.replace('SH','SS')




def _cleanStockId(s):
    '''
    :param str:number
    :return:
    '''
    s=str(s)
    #or s=s.zfill(6)
    return '0'*(6-len(s))+s

def cleanStockId(stockIds):
    if isinstance(stockIds,str):
        return _cleanStockId(stockIds)
    else:
        newStockIds=[]
        for stockId in stockIds:
            newStockIds.append(_cleanStockId(stockId))
        return newStockIds


