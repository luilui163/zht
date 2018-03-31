# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 10:03:27 2016

@author: hp
"""

def normalize_date(date):
    '''
    normalize date with form in '2016-03-09' or '2012/3/6'
    '''
    
    if '-' in date:
        year,month,day=tuple(date.split('-'))
    elif r'/' in date:
        year,month,day=tuple(date.split(r'/'))
        
    if len(month)==1:
        month='0'+month
    if len(day)==1:
        day='0'+day
    return year+month+day
    
