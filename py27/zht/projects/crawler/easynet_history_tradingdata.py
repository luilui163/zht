#-*-coding: utf-8 -*-
#@author:tyhj

import urllib2
import urllib
import os

directory=r'C:\data\history_trading_data'
stocknames=open('stocknames.txt').read().split('\n')
stockids=[s[:6] for s in stocknames]

for id in stockids:
    url = 'http://quotes.money.163.com/service/chddata.html?code=0%s&start=20000720&end=20161114' % id
    response = urllib2.urlopen(url)
    headers = response.info()
    totalsize = int(headers['Content-Length'])
    if totalsize<118:
        url = 'http://quotes.money.163.com/service/chddata.html?code=1%s&start=20000720&end=20161114' % id
    urllib.urlretrieve(url, os.path.join(dir, '%s.csv' % id))
    print id


# def callbackfunc(blocknum, blocksize, totalsize):
#     '''回调函数
#     @blocknum: 已经下载的数据块
#     @blocksize: 数据块的大小
#     @totalsize: 远程文件的大小
#     '''
#     percent = 100.0 * blocknum * blocksize / totalsize
#     if percent > 100:
#         percent = 100
#     print "%.2f%%"% percent,blocknum,blocksize,totalsize

# id='000428'
# url = 'http://quotes.money.163.com/service/chddata.html?code=0%s&start=20000720&end=20161114' % id
# a=urllib.urlretrieve(url, os.path.join(directory, '%s.csv' % id),callbackfunc)















