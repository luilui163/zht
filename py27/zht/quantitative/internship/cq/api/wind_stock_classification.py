# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:33:19 2016

@author: Administrator
"""

from WindPy import *
from datetime import *
import os
import time
w.start()

stocks=w.wset("sectorconstituent","date=%s;sectorid=a001010100000000"%time.strftime('%Y%m%d',time.localtime(time.time()))).Data[1]
classification={1:'sw',2:'wind',3:'zx',4:'gx'}

def get_classification_history(folder,date):
    for industryType in [1,2,3,4]:
        industrys=w.wsd(stocks, "industry2", date, date, "industryType=%d;industryStandard=5"%industryType).Data[0]
        if len(industrys)>5:
            filepath=os.path.join(folder,classification[industryType])
            if not os.path.isdir(filepath):
                os.makedirs(filepath)
            with open(os.path.join(filepath,r'%s.txt'%date),'w') as f:
                for i in range(len(stocks)):
                    f.write('%s\t%s\n'%(stocks[i].encode('gb2312'),industrys[i].encode('gb2312')))
        else:
            print '%s is not weekday.There is no data for this day.'%date
            


def run(folder,startdate,enddate):
    sd=datetime.strptime(startdate,'%Y%m%d')
    ed=datetime.strptime(enddate,'%Y%m%d')
    oneday=timedelta(days=1)
    dates=[]
    dates.append(startdate)
    while sd!=ed:
        sd+=oneday
        dates.append(datetime.strftime(sd,'%Y%m%d'))
    for date in dates:
        get_classification_history(folder,date)
        print date
        
if __name__=='__main__':
    folder=r'c:\test'
    startdate='20160831'
    enddate='20160904'
    run(folder,startdate,enddate)

