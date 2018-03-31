# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-10  15:10
# NAME:assetPricing-fileu.py
import os
import time
import datetime

def get_modification_time(fp):
    '''
    modification date
    :param fp:
    :return:
    '''
    mtime=os.stat(fp).st_mtime
    mtime=time.localtime(mtime)
    return datetime.datetime(*mtime[:6])

def get_intersection_fns(dp1,dp2):
    '''
    get the intersection of files for two directorys
    :param dp1:
    :param dp2:
    :return:sorted list
    '''
    fns1=os.listdir(dp1)
    fns2=os.listdir(dp2)
    inter=set(fns1).intersection(set(fns2))
    return sorted(list(inter))


