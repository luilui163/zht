# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-11  14:35
# NAME:assetPricing-stocku.py


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



