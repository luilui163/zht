# -*- coding:utf-8 -*-
import threading
from EmQuantAPI import *
import time


date=time.strftime('%Y%m%d',time.localtime(time.time()))

def startCallback(message):
    print "[EmQuantAPI Python]", message
    return 1

def myQuoteCallback(quantdata):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    datepath=r'e:\data\marketdata\%s'%date
    if not os.path.isdir(datepath):
        os.makedirs(datepath)
    for i in range(0, len(quantdata.Codes)):
        try:
            fl=open(os.path.join(datepath,quantdata.Codes[i][:-3])+'.txt','a')
            fl.write(','.join(map(str,quantdata.Data[quantdata.Codes[i]])))
            fl.write('\n')
        except:
            fl=open(os.path.join(datepath,quantdata.Codes[i][:-3]+'.txt'),'w')
            fl.write(','.join(map(str, quantdata.Data[quantdata.Codes[i]])))
            fl.write('\n')
        fl.close()
    print quantdata.Data[quantdata.Codes[0]][0]

stocks=open('medium_and_small.txt').read().split('\n')[:-1][:300]
items=open('items.txt').read().split('\n')[:-1]

loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
# for i in range(10):
#     c.csq(','.join(stocks[:30+i*30]),','.join(items),'Pushtype=1',myQuoteCallback)
data=c.csq(','.join(stocks),','.join(items),'PushType=1',myQuoteCallback)
raw_input("press any key to cancel csq")
c.csqcancel(0)

#Multithreading
# stockIds=[stocks[:100+100*i] for i in range(3)]
# threads=[]
# for i in range(3):
#     th = threading.Thread(target=c.csq, args=[','.join(stockIds[i]),','.join(items),'PushType=1',myQuoteCallback])
#     threads.append(th)
# for j in range(len(threads)):
#     threads[j].start()
# for k in range(len(threads)):
#     threads[k].join()


# datacsc=c.csc('300059.SZ','OPEN,CLOSE,HIGH','2016-11-9','2016-11-10')



# try:
#       #输入订阅的代码和指标
#       data = c.csq(','.join(stocks), ','.join(items), "Pushtype=1",myQuoteCallback)
# except:
#       loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
#       #输入订阅的代码和指标
#       data = c.csq(','.join(stocks), ','.join(items), "Pushtype=1", myQuoteCallback)
# #任意按键，使程序停止运行
# raw_input("press any key to cancel csq")
# c.csqcancel(0)





