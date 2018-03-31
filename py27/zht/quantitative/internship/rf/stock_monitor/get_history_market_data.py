#-*-coding: utf-8 -*-
#@author:tyhj
from EmQuantAPI import *
import time
import tool
import os
import pandas as pd


def get_tradedates(startdate='20090101'):
    enddate=time.strftime('%Y%m%d',time.localtime(time.time()))
    tradedates=c.tradedates(startdate,enddate).Data
    with open('tradedates.txt','w') as f:
        for td in tradedates:
            f.write(tool.normalize_date_format(td)+'\n')

# if __name__=='__main__':
#     loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
#     tradedates=open('tradedates.txt').read().split('\n')[:-1]
#     stocknames=open('stocklist.txt').read().split('\n')[:-1]
#
#     cwd=os.getcwd()
#     indicators=open(os.path.join(cwd,r'marketdata\indicators.txt')).read().split('\n')
#
#     for stockname in stocknames:
#         flag=1
#         while flag:
#             try:
#                 df=pd.DataFrame(columns=indicators)
#                 for i,d in enumerate(tradedates):
#                     #前复权数据
#                     data = c.css(codes=stockname, indicators=','.join(indicators),
#                                  options='Tradedate=%s,AdjustFlag=3' % d).Data[stockname]
#                     df.loc[d]=data
#                     print stockname,d,data
#                 df.to_csv(os.path.join(cwd,r'marketdata\%s.csv'%stockname))
#                 flag=0
#             except:
#                 loginResult = c.start('rflh0000', '719181', "ForceLogin=1")


loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
tradedates = open('tradedates.txt').read().split('\n')[:-1]
stocknames = open('stocklist.txt').read().split('\n')[:-1]

cwd = os.getcwd()
indicators = open(os.path.join(cwd, r'marketdata\indicators.txt')).read().split('\n')

def initialises_df(stocklist):
    #initialises the df for every stock
    for stock in stocklist:
        df=pd.DataFrame(columns=indicators)
        df.to_csv(os.path.join(cwd, r'marketdata\%s.csv' % stock))



def get_history_marketdata():
    for tradedate in tradedates:
        flag=1
        while flag:
            try:
                data = c.css(codes=','.join(stocknames), indicators=','.join(indicators), \
                             options='Tradedate=%s,AdjustFlag=3' % tradedate).Data
                flag=0
            except Exception as e:
                print e
                loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
        for sn in stocknames:
            df=pd.read_csv(os.path.join(cwd, r'marketdata\%s.csv' % sn),index_col=0)
            df.loc[tradedate]=data[sn]
            df.to_csv(os.path.join(cwd, r'marketdata\%s.csv' % sn))
            print tradedate,sn

