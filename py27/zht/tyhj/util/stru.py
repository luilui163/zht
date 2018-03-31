#-*-coding: utf-8 -*-
#@author:tyhj


def extractDate(dateStr):
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









