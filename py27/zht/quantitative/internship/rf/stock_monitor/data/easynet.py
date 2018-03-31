#-*-coding: utf-8 -*-
#@author:tyhj

import urllib
import urllib2
import pandas as pd
import time


today=time.strftime('%Y%m%d',time.localtime(time.time()))
url=r'http://quotes.money.163.com/service/chddata.html?code=0601398&start=20000720&end=%s'%today
urllib.urlretrieve(url,'test.csv')
df=pd.read_csv('test.csv',index_col=0)










