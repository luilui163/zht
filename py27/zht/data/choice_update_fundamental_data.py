from EmQuantAPI import *
import datetime
import tool
import os
import pandas as pd
import csv


date=datetime.date.today()
date=date.strftime('%Y%m%d')

loginResult = c.start('rflh0000', '719181', "ForceLogin=1")

stocklist=open(r'stocklist.txt').read().split('\n')[:-1]

with open(r'jlr.txt','w') as f:
    data1=c.css(codes=','.join(stocklist),indicators='ESTNI',options='PredictYear=2016,EndDate=%s'%date).Data
    data2=c.css(codes=','.join(stocklist),indicators='ESTNI',options='PredictYear=2017,EndDate=%s'%date).Data
    for code in stocklist:
        f.write('%s\t%s\t%s\n'%(code,data1[code][0],data2[code][0]))
        print code

with open('roe.txt','w') as f:
    roe1=c.css(codes=','.join(stocklist),indicators='ROEAVG',options='ReportDate=20160331').Data
    roe2 = c.css(codes=','.join(stocklist), indicators='ROEAVG', options='ReportDate=20160630').Data
    roe3 = c.css(codes=','.join(stocklist), indicators='ROEAVG', options='ReportDate=20160930').Data
    f.write('code\t20160331\t20160630\t20160930\n')
    for code in stocklist:
        f.write('%s\t%s\t%s\t%s\n'%(code,roe1[code][0],roe2[code][0],roe3[code][0]))
        print code

with open('yoygr.txt','w') as f:
    yoygr1=c.css(codes=','.join(stocklist),indicators='YOYGR',options='ReportDate=20160630').Data
    yoygr2=c.css(codes=','.join(stocklist),indicators='YOYGR',options='ReportDate=20160930').Data
    f.write('code\t20160630\t20160930\n')
    for code in stocklist:
        f.write('%s\t%s\t%s\n'%(code,yoygr1[code][0],yoygr2[code][0]))
        print code

with open('mv.txt','w') as f:
    date=datetime.date.today()-datetime.timedelta(1)
    date=date.strftime('%Y%m%d')
    mv=c.css(codes=','.join(stocklist),indicators='MV',options='TradeDate=%s'%date).Data
    f.write('code\t%s\n'%date)
    for code in stocklist:
        f.write('%s\t%s\n'%(code,mv[code][0]))
        print code




