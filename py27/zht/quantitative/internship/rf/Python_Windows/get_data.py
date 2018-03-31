# -*- coding:utf-8 -*-
from EmQuantAPI import *

def startCallback(message):
    print "[EmQuantAPI Python]", message
    return 1

def demoQuoteCallback(quantdata):
    """
    DemoCallback 是EM_CSQ订阅时提供的回调函数模板。该函数只有一个为c.EmQuantData类型的参数quantdata
    :param quantdata:c.EmQuantData
    :return:
    """
    print "demoQuoteCallback,", str(quantdata)


loginResult = c.start('rflh0000', '719181', "ForceLogin=0")

def get_tradedates():
    tradedates=c.tradedates('20060101','20161018')
    with open(r'c:\zht\tradedates.txt','w') as f:
        for d in tradedates.Data:
            f.write(d+'\n')
            print d

dates=open(r'c:\zht\tradedates.txt').read().split('\n')[:-1]
#
# def change_date_format(d):
#     year,month,day=d.split(r'/')
#     if len(month)<2:
#         month='0'+month
#     if len(day)<2:
#         day='0'+day
#     new_date=year+month+day
#     return new_date
# with open(r'c:\zht\date.txt','w') as f:
#     for d in dates:
#         new_date=change_date_format(d)
#         f.write(new_date+'\n')
#         print d

# with open()

# for PE,PB,PS,the type is 7,a.e the newest annual report
d=dates[-1]
data1=c.css('000001.SZ','MV,FREEFLOATMV,DifferM,TurnM,PE,PB,PS,BETAR24M,ANNUSTDEVRR24M','TradeDate=%s,Type=7'%d)
print data1

















