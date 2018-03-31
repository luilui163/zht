#-*-coding: utf-8 -*-
#@author:tyhj
import os
from data.config import DATA_BASE_DIR

def getStockDfPath(stockId):
    '''
    get market data path of the stockId in database
    :param stockId:
    :return:
    '''
    path=os.path.join(DATA_BASE_DIR,stockId+'.csv')
    return path


#获取当前路径
def get_dirpath():
    cwd=os.getcwd()
    dirpath=os.path.join(os.path.split(cwd)[0])
    return dirpath
dirpath=get_dirpath()











