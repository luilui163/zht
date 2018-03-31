#-*-coding: utf-8 -*-
#@author:tyhj

import os
import pandas as pd

def parse_stock_data():
    path=r'C:\data\gx\rawdata\stock_hfq'
    file_names=os.listdir(path)
    for i,fn in enumerate(file_names):
        df=pd.read_csv(os.path.join(path,fn),sep='\t', \
                       names=['open','high','low','close','volume','amount'], \
                       index_col=0,skiprows=[0,1])
        df=df[:-1]
        code=fn[3:-4]+'.'+fn[:2]
        df.to_csv(r'C:\data\gx\csvdata\stock_hfq\%s.csv'%code)
        print 'complete %d/%d'%(i+1,len(file_names))

def parse_index_data():
    path=r'C:\data\gx\rawdata\index_hfq'
    file_names=os.listdir(path)
    for i,fn in enumerate(file_names):
        df=pd.read_csv(os.path.join(path,fn),sep='\t', \
                       names=['open','high','low','close','volume','amount'], \
                       index_col=0,skiprows=[0,1])
        df=df[:-1]
        code=fn[3:-4]
        df.to_csv(r'C:\data\gx\csvdata\index_hfq\%s.csv'%code)
        print 'complete %d/%d'%(i+1,len(file_names))


def parseSrc():
    path=r'D:\quantDb\sourceData\gx'
    file_names = os.listdir(path)
    for i, fn in enumerate(file_names):
        df = pd.read_csv(os.path.join(path, fn), sep='\t', \
                         names=['open', 'high', 'low', 'close', 'volume', 'amount'], \
                         index_col=0, skiprows=[0, 1])
        df = df[:-1]
        code = fn[:6]
        df.to_csv(r'D:\quantDb\mkt\daily\gx\%s.csv' % code)
        print 'complete %d/%d' % (i + 1, len(file_names))













