
# -*- coding:utf-8 -*-

__author__ = 'Administrator'


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


loginResult = c.start('username', 'password', "ForceLogin=0")

# csd 使用范例
c.csd("300059.SZ,600425.SH", "open,close", "2016-07-01", "2016-07-06", "period=1,adjustflag=1,curtype=1,pricetype=1,year=2016")
data = c.csd("300059.SZ,600425.SH", "open,close", "2016-07-01", "2016-07-06")
if data.ErrorCode != 0:
    print "request csd Error, ", data.ErrorMsg
else:
    print "csd输出结果======分隔线======"
    for code in data.Codes:
        for i in range(0, len(data.Indicators)):
            for j in range(0, len(data.Dates)):
                print data.Data[code][i][j]

# css使用范例
c.css("300059.SZ", "open,close", "Period=1,AdjustFlag=1,CurType=1,PriceType=1,ReportDate=20140930,TradeDate=20160217,StartDate=2015/02/10,EndDate=2015/03/10,ItemsCode=9,type=1,Cycle=1")
data = c.css("300059.SZ", "open,close")
if data.ErrorCode != 0:
    print "request csd Error, ", data.ErrorMsg
else:
    print "css输出结果======分隔线======"
    for code in data.Codes:
        for i in range(0, len(data.Indicators)):
                print data.Data[code][i]

# sector使用范例
data = c.sector("011019002001", "2016-04-26")
# 011019002001 申万-保险行业
if data.ErrorCode != 0:
    print "request csd Error, ", data.ErrorMsg
else:
    print "sector输出结果======分隔线======"
    for code in data.Data:
        print code

# tradedate使用范例
data = c.tradedates("2016-07-01", "2016-07-12")
print "tradedate输出结果======分隔线======"
for item in data.Data:
    print item

# getdate使用范例
print "getdate输出结果======分隔线======"
data = c.getdate("20160426", -3, "Market=CNSESH")
print data.Data

#实时行情订阅使用范例
print "csq输出结果======分隔线======"
data = c.csq("300059.SZ,002716.SZ,600834.SH,600616.SH", "PRECLOSE,OPEN,HIGH,LOW,NOW,AMOUNT", "Pushtype=1", demoQuoteCallback)
text = raw_input("press any key to cancel csq \r\n")
#取消订阅
data = c.csqcancel(data.SerialID)

#退出
data = logoutResult = c.stop()
print 'ok'
