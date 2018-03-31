#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import os
from zht.data import data_handler,df_handler
from zht import tool
import shutil

def daily_return():
    path=r'c:\db\mkt\daily\returns'
    ret=data_handler.get_return_df()
    dates=list(ret.index)
    for date in dates:
        df=ret.loc[[date]]
        df=df.T
        df=df.dropna()
        if len(df)>0:
            df.to_csv(os.path.join(path,date+'.csv'))
        print date

def daily_return_ts():
    pathSave=r'C:\db\mkt\time_series\returns'
    codes=data_handler.get_code_list()
    for code in codes:
        df=data_handler.get_df(code)
        pct=df[['close']].pct_change()
        pct=pct.dropna(axis=0)
        if len(pct)>0:
            pct.columns=['return']
            pct.to_csv(os.path.join(pathSave,code+'.csv'))
        print code

def _get_comoment_ts(history_window=250):
    path = r'C:\db\factors\time_series\comoment'
    benchmark = data_handler.get_index_df(database_path=r'C:\db\mkt\daily\index')
    codes = data_handler.get_code_list()

    for code in codes:
        stock = data_handler.get_df(code)
        combine = stock[['close']]
        combine['benchmark'] = benchmark['close']
        ret = combine.pct_change()
        ret = ret.dropna(axis=0)

        comoment_df = pd.DataFrame(columns=['cov', 'cos', 'cok'])
        for i in range(history_window, len(ret)):
            df = ret[i - history_window:i]
            # r = ret.at[ret.index[i], 'close']
            cov = tool.Cov(df)
            cos = tool.Cos(df)
            cok = tool.Cok(df)
            comoment_df.loc[ret.index[i]] = [cov, cos, cok]
        comoment_df.to_csv(os.path.join(path, code + '.csv'))
        print code


#TODO:这种计算处理方式太慢，参看df_handler.ts_to_cross
def get_comoment_factors():
    _get_comoment_ts()
    #time series to cross sectional df
    path = r'C:\db\factors\time_series\comoment'
    pathtmp=r'c:\db\factors\daily\comoment\tmp'
    if not os.path.exists(pathtmp):
        os.makedirs(pathtmp)
    fns=os.listdir(path)
    dates=list(data_handler.get_index_df(database_path=r'C:\db\mkt\daily\index').index)
    for date in dates:
        df=pd.DataFrame()
        for fn in fns:
            com=pd.read_csv(os.path.join(path,fn),index_col=0)
            try:
                s=com.loc[date]
                df[fn[:-4]]=s
            except:
                pass
        df=df.T
        if len(df)>0:
            df.to_csv(os.path.join(pathtmp,date+'.csv'))
        print date

    #split the df into 3 subdfs
    fns=os.listdir(pathtmp)
    factornames=['cov', 'cos', 'cok']
    for factorname in factornames:
        pathsave = os.path.join(r'C:\db\factors\daily\comoment', factorname)
        if not os.path.exists(pathsave):
            os.makedirs(pathsave)

    for fn in fns:
        df=pd.read_csv(os.path.join(pathtmp,fn),index_col=0)
        for factorname in factornames:
            subdf=df[[factorname]]
            subdf.to_csv(os.path.join(r'C:\db\factors\daily\comoment',factorname,fn))
        print fn

    shutil.rmtree(pathtmp)


def base_stats_ts():
    history_window=250
    tsPath=r'C:\db\mkt\time_series\returns'
    pathSave=r'c:\db\mkt\time_series'
    fns=os.listdir(tsPath)
    for fn in fns:
        df=pd.read_csv(os.path.join(tsPath,fn),index_col=0)
        if len(df)>history_window:
            avg=df.rolling(history_window,min_periods=int(history_window*0.5)).mean()
            var = df.rolling(history_window, min_periods=int(history_window * 0.5)).var()
            skew=df.rolling(history_window,min_periods=int(history_window*0.5)).skew()
            kurt=df.rolling(history_window,min_periods=int(history_window*0.5)).kurt()
            avg.to_csv(os.path.join(pathSave,'returnAvg',fn))
            var.to_csv(os.path.join(pathSave,'returnVar',fn))
            skew.to_csv(os.path.join(pathSave,'returnSkew',fn))
            kurt.to_csv(os.path.join(pathSave,'returnKurt',fn))
        print fn


def get_base_stats_cross():
    factorPath = r'c:\db\mkt\time_series'
    for factorName in ['returnAvg', 'returnVar', 'returnSkew', 'returnKurt']:
        path = os.path.join(factorPath, factorName)
        pathSave = os.path.join(r'C:\db\factors\daily\base_stats', factorName)
        if not os.path.exists(pathSave):
            os.makedirs(pathSave)

        df = df_handler.merge_all(path)
        dates = list(df.index)
        for date in dates:
            subdf = df.loc[[date], :]
            subdf = subdf.T
            subdf = subdf.dropna()
            subdf.to_csv(os.path.join(pathSave, date + '.csv'))
            print factorName, date








