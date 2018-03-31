#-*-coding: utf-8 -*-
#@author:tyhj
import os
from tyhj.data.config import DATA_BASE_DIR

def getStockDfPath(stockId):
    '''
    get market data path of the stockId in database
    :param stockId:
    :return:
    '''
    path=os.path.join(DATA_BASE_DIR,stockId+'.csv')
    return path














