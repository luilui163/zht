#-*-coding: utf-8 -*-
#@author:tyhj

from bs4 import BeautifulSoup
import urllib2
import time

'''
收盘后抓取
http://finance.sina.com.cn/money/forex/hq/DINIW.shtml
'''

date=time.strftime("%Y%m%d",time.localtime(time.time()))
url='http://quote.eastmoney.com/qihuo/DINI.html'
content=urllib2.urlopen(url).read().decode('gb2312')
soup=BeautifulSoup(content)
tr=soup.find_all('tr',{'class':'tline'})[0]



