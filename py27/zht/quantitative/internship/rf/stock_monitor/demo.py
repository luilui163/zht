
# -*- coding:utf-8 -*-

__author__ = 'Administrator'


from EmQuantAPI import *

def startCallback(message):
    print "[EmQuantAPI Python]", message
    return 1
#在E盘里生成Callback.txt文件
def demoQuoteCallback(quantdata):
    for i in range(0, len(quantdata.Codes)):
          try:
             fl=open('E:/Callback.txt', 'a')
             fl.write(str(quantdata.Codes[i])+" :"+str(quantdata.Data[quantdata.Codes[i]]))
             fl.write("    ")
             fl.write("\n")
          except:
             fl=open(r'E:/Callback.txt', 'w')
             fl.write(str(quantdata.Codes[i])+" :"+str(quantdata.Data[quantdata.Codes[i]]))
             fl.write("\n")
    fl.close()



#主函数

#输入用户名和密码，except里也需要输入
loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
try:
      #输入订阅的代码和指标
      data = c.csq("300059.SZ,600000.SH", "TIME,OPEN,HIGH,LOW,Now", "Pushtype=1",demoQuoteCallback)
except:
      loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
      #输入订阅的代码和指标
      data = c.csq("300059.SZ,600000.SH", "TIME,OPEN,HIGH,LOW,Now", "Pushtype=1",demoQuoteCallback)
#任意按键，使程序停止运行
raw_input("press any key to cancel csq")
c.csqcancel(0)

