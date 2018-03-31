#-*-coding: utf-8 -*-
#@author:tyhj

def _containCN(str):
    str=str.decode('gb2312') #the encoding for RESSET data is gb2312
    for ch in str:
        if u'\u4e00'<=ch<=u'\u9fff':
            return True
    return False

def _rename(str):
    items=str.split('_')
    validItems=[]
    for item in items:
        if not _containCN(item):
            validItems.append(item)
    return '_'.join(validItems)

def rename(s):
    if isinstance(s,str):
        return _rename(s)
    else:
        newnames=[]
        for ss in s:
            newnames.append(_rename(ss))
        return newnames












