# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 14:30:36 2016

@author: Administrator
"""

import urllib
import datetime

def download_stock_data(stock_list):
    for sid in stock_list:
        url='http://table.finance.yahoo.com/table.csv?s='+sid
        fname='c:\\data\\yahoo\\'+sid+'.csv'
        print 'downloading %s from %s'%(fname,url)
        urllib.urlretrieve(url,fname)
        
        
def download_stock_in_period(stock_list,start,end):
    for sid in stock_list:
        params={'a':start.month-1,'b':start.day,'c':start.year,
                'd':end.month-1,'e':end.day,'f':end.year,
                's':sid}
        url='http://table.finance.yahoo.com/table.csv?'
        qs=urllib.urlencode(params)
        url=url+qs
        fname='c:\\data\\yahoo\\'+'%s_%d%d%d_%d%d%d.csv'%(sid,start.year,start.month,start.day,end.year,end.month,end.day)
        print 'downloading %s from %s'%(fname,url)
        urllib.urlretrieve(url,fname)
    

if __name__=='__main__':
    stock_list=['000001.sz','300001.sz']
    start=datetime.date(year=2015,month=12,day=17)
    end=datetime.date(year=2016,month=9,day=19)
#    download_stock_data(stock_list)
    download_stock_in_period(stock_list,start,end)
    
##注意如果股票代码没有时候，返回的是html，可以用urlopen来控制