#-*-coding: utf-8 -*-
#@author:tyhj
from sklearn import datasets,linear_model
import pandas as pd
import numpy as np
from zht.data import data_handler
from datetime import datetime
import time
import math


length=250
def get_df():
    df=data_handler.get_return_df()
    df=df.dropna(axis=1,thresh=length*0.6)
    df.index=[pd.to_datetime(ind) for ind in df.index]
    return df

def get_month_end(df):
    start_date=df.index[length]
    end_date=df.index[-1]
    month_ends=pd.date_range(start_date,end_date,freq='M')
    return month_ends

def calculate_DASTD(df,month_end):
    #for one month
    df_sub=df.loc[:month_end]
    df_sub=df_sub[-length:]
    df_sub=df_sub.dropna(axis=1,thresh=length*0.6)
    df_sub=df_sub.dropna(axis=1,how='any')
    ewm = [pow(0.5, i/40.0) for i in range(1, 1+length)[::-1]]
    w=np.matrix(ewm)
    dastd={}
    for code in df_sub.columns[:-1]:
        para=calculate_para(df_sub,code)
        para=np.matrix(para)
        r=w*np.matrix(para).T
        dastd[code]=math.sqrt(r.getA()[0][0])
    dastd=pd.DataFrame(dastd,index=[month_end])
    return dastd

def calculate_para(df_sub,code):
    mean=df_sub[code].mean()
    aa=df_sub[code]-mean
    return pow(aa,2)

def get_DASTD():
    df=get_df()
    month_ends=get_month_end(df)
    dastd=pd.DataFrame(columns=df.columns[:-1])
    for month_end in month_ends:
        r=calculate_DASTD(df,month_end)
        dastd=dastd.append(r)
        print month_end
    return dastd



def get_start_and_end_point(df):
    start_date=df.index[0]
    end_date=df.index[-1]
    month_ends=pd.date_range(start_date,end_date,freq='M')
    month_starts=pd.date_range(start_date,end_date,freq='MS')
    #the month_start and month_end may not be corresponding,the for line above used to
    #solve this problem
    start_date_adjust=month_starts[0]
    end_date_adjust=month_ends[-1]
    month_ends=pd.date_range(start_date_adjust,end_date_adjust,freq='M')
    month_starts = pd.date_range(start_date_adjust, end_date_adjust, freq='MS')
    return zip(month_starts,month_ends)

def calculate_CMRA(sub_df):
    '''
    :param sub_df: the last 12 months' data
    :return: Z
    '''
    sep=get_start_and_end_point(sub_df)
    ln_df=pd.DataFrame()
    for s in sep:
        tmp_df=sub_df.loc[s[0]:s[1]]
        tmp_df=tmp_df.dropna(axis=1,thresh=15) #delete those stocks with too little data in this month
        month_return=tmp_df.sum()
        month_return_df=pd.DataFrame(month_return,columns=[s[1]])
        month_return_df=month_return_df.T
        ln_df=ln_df.append(np.log(month_return_df+1))
    max=ln_df.max()
    min=ln_df.min()
    cmra=np.log(1+max)-np.log(1+min)
    # cmra=pd.DataFrame(cmra,columns=[sep[-1][1]]).T
    return cmra

def get_CMRA():
    df=get_df()
    start_and_end_point=get_start_and_end_point(df)
    CMRA=pd.DataFrame()
    for i in range(12,len(start_and_end_point)):
        #notice that .ix and .iloc are different,.ix includes the last element,while .iloc doesn't
        #so it is i-11,rather than i-12
        sub_df=df.ix[start_and_end_point[i-11][0]:start_and_end_point[i][1]]
        cmra=calculate_CMRA(sub_df)
        month_end=start_and_end_point[i][1]
        CMRA[month_end]=cmra
        print month_end
    CMRA=CMRA.T
    return CMRA


def run():
    DASTD=get_DASTD()
    CMRA=get_CMRA()
    DASTD.to_csv(r'C:\data\gx\csvdata\factors\DASTD.csv')
    CMRA.to_csv(r'c:\data\gx\csvdata\factors\CMRA.csv')
    # for HSIGMA,refer to the script beta_hsigma
if __name__=='__main__':
    run()




