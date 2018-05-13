# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-10  15:26
# NAME:assetPricing-listu.py

import numpy as np

def chunkify(l,n):
    '''
    split a list or array into n parts of approximately equal
    length.refer to https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length

    :param l:list or array
    :param n:
    :return:
    '''

    k, m = divmod(len(l), n)
    return (l[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def chunkifyByBreakPoints(lst,breakPoints):
    '''
    splitting a list into N parts according the breakPoints

    examples:
    >>chunkifyByBeakPoints(range(15),[0.3,0.7])
      [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14]]

    Args:
        lst:
        breadPoints: list

    Returns:

    '''
    ns=[0]
    ns+=[int(point*len(lst)) for point in breakPoints]
    ns+=[len(lst)]
    sublist=[lst[ns[i-1]:ns[i]] for i in range(1,len(ns))]
    return sublist

def group_with(lst, func=lambda x: x):
    '''
    group the list by applying func
    Args:
        lst:
        func:

    Returns:dict

    '''

    key = {}
    for initial, transformed in zip(lst, map(func, lst)):
        key[transformed] = [] if transformed not in key else key[
            transformed]
        key[transformed].append(initial)
    return key
