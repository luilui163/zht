# -*- coding:utf-8 -*-
'''
Create date 	: 2016/05/16
Author		: kaihao
Update date	: 2016/05/17
Description	: Get 转送比例
'''

import datetime,time
import string
import urllib,urllib2

from bs4 import BeautifulSoup 
#from pyh import *
import csv

'''
常用打印显示信息函数
'''
#Description : Get Current Date and Time
def GetDateTime():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#Description : Get Current Date
def GetDate():
	return datetime.datetime.now().strftime("%Y-%m-%d")

'''
Description : Get Data Of Song Zhuan bi li From Eastmoney
Input	: year, quarter( 1 - annual, 0 - semi-annual)
Output	: data list 
Note	: 查询子函数 
'''

def get_szbl(gyear, gq):
	#Date gq = 1
	gmd	= '12-31' if gq > 0 else '06-30' 
	gjidu 	= '%d-' % gyear + gmd

	#Generate 高转送 Jason url
	params = urllib.urlencode({'sr': -1, 'st': 10, 'p': 1, 'ps': 3000, 'fd': gjidu})
	url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=SZBL&%s' % (params)
	#Get HTML 
	try:
		html = urllib2.urlopen(url).read()
	except:
		print '<HTTP> GET So Frequently,Need Sleep!'
		time.sleep(100) 
		html = urllib2.urlopen(url).read()
	time.sleep(3)	
	
	#Jason 解析
	glist = html[3:-3].split('","')

	gstocklist = []
	for item in glist:
		gstock = item.split(',')
		# 
		gstocklist.append(gstock)

	return gstocklist

'''
Descreption : Save Data to CSV
'''
def csvSZBL():
	with open(r'c:/garbage/test.csv', 'w') as gcsv:
		gwriter = csv.writer( gcsv )
		for gyear in range(2015, 2016): 
			print '[%s] Begin %d ' % (GetDateTime(), gyear)
			gwriter.writerows(get_szbl( gyear, 1))
			print '[%s] Download %d Annual Data' % (GetDateTime(), gyear)
			gwriter.writerows(get_szbl( gyear, 0))
			print '[%s] Download %d semi-Annual Data' % (GetDateTime(), gyear)
	
	gcsv.close()	

if __name__ == '__main__':
	csvSZBL()




