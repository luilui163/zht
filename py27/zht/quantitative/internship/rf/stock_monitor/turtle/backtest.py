#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
import numpy as np
import os
from data import dataAPI



# matpath=r'C:\zht\OneDrive\script\rf\stock_monitor\turtle\data\A_Day'
df=dataAPI.get_data('000019.SZ')
def initialize():
    df['cash']=np.NaN
    df['cash'][0]=10000000
    df['floating_profit']=np.NaN
    df['floating_profit'][0]=0.0
    df['position']=np.NaN
    df['position'][0]=0
    df['last_deal_price']=np.NaN

def check_position(i):
    if df['position'][i]>0:
        return 1
    elif df['position'][i]<0:
        return -1
    else:
        return 0

def signal_in():
    df['band_up']=df['high'].rolling(10).max()
    df['band_down']=df['low'].rolling(10).min()
    df['signal'] = np.NaN
    for i in range(1,len(df)):
        if df['close'][i]>df['band_up'][i]:
            df['signal'][i]=1
        elif df['close'][i]<df['band_down'][i]:
            df['signal'][i]=-1
        else:
            df['signal'][i]=0

def calculate_N():
    df['true_range']=np.NaN
    df['N']=np.NaN
    for i in range(1,len(df)):
        a1=df['high'][i]-df['low'][i]
        a2=df['high'][i]-df['close'][i-1]
        a3=df['close'][i-1]-df['low'][i]
        df['true_range'][i]=max(a1,a2,a3)
    # for i in range(1,len(df)):
    #     df['N'][i]=np.mean(df['N'][i-20:i]+df['true_range'][i])
    df['N']=df['true_range'].rolling(20).mean()

def calculate_unit():
    df['unit']=np.NaN
    for i in range(1,len(df)):
        df['unit'][i]=df['cash'][i]*0.01/df['N']

def add_or_stop():
    df['add_position']=np.NaN
    for i in range(1,len(df)):
        if check_position(i)==1 and df['close'][i]>(df['last_deal_price'][i]+0.5*df['N']):
            df['add_position']=1
        else:
            df['add_position']=0

def stop_loss():
    df['stop_loss']=np.NaN
    for i in range(1,len(df)):
        if check_position(i)==1 and df['close'][i]<(df['last_deal_price'][i]-2*df['N'])
            df['stop_loss']=1
        else:
            df['stop_loss']=0

def stop_profit():
    df['stop_profit']=np.NaN
    for i in range(1,len(df)):
        if check_position(i)==1 and df['close'][i]<df['band_down'][i]:
            df['stop_profit'][i]=1
        else:
            df['stop_profit'][i]=0


def run():
    initialize()
    in_or_out()











