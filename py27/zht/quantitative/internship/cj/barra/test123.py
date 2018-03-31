#-*-coding: utf-8 -*-
#@author:tyhj

import os
import pandas as pd
import numpy as np
from zht.data import df_handler
from zht.data import file_handler
#-----------------------------------------
#growth
#TODO: 计算growth值时候，少了一个子类研报中有三个指标合成，但是这里只有两个
def normalize_growth():
    path=r'C:\data\barra_factors\growth'
    directorys=os.listdir(path)
    for directory in directorys:
        if not os.path.isdir(os.path.join(r'C:\data\barra_factors_normalized\growth',directory)):
            os.makedirs(os.path.join(r'C:\data\barra_factors_normalized\growth',directory))

        filenames=os.listdir(os.path.join(path,directory))
        for fn in filenames:
            df=pd.read_csv(os.path.join(path,directory,fn),index_col=0)
            df=df_handler.normalize(df)
            df.to_csv(os.path.join(r'C:\data\barra_factors_normalized\growth',directory,fn))
        print directory

def combined_the_growth_subfactors():
    path=r'C:\data\barra_factors_normalized\growth'
    if not os.path.isdir(r'c:\data\barra_factors_combined\growth'):
        os.makedirs(r'c:\data\barra_factors_combined\growth')

    date_intersection=file_handler.get_date_intersection(path)

    directorys=os.listdir(path)
    for date in date_intersection:
        df=pd.DataFrame()
        for directory in directorys:
            sub_df=pd.read_csv(os.path.join(path,directory,'%s.csv'%date),index_col=0)
            df=df.append(sub_df)
        df=df.mean(axis=1)
        df=pd.DataFrame(df,columns=['growth'])
        df.to_csv(os.path.join(r'c:\data\barra_factors_combined\growth','%s.csv'%date))
        print date
#-----------------------------------------
#EP
def normalize_EP():
    path=r'C:\data\barra_factors\EP'
    directorys=os.listdir(path)
    for directory in directorys:
        if not os.path.isdir(os.path.join(r'C:\data\barra_factors_normalized\EP',directory)):
            os.makedirs(os.path.join(r'C:\data\barra_factors_normalized\EP',directory))

        filenames=os.listdir(os.path.join(path,directory))
        for fn in filenames:
            df=pd.read_csv(os.path.join(path,directory,fn),index_col=0)
            df=1/df  #since the initial df is PE,we need to get EP
            df=df_handler.normalize(df)
            df.to_csv(os.path.join(r'C:\data\barra_factors_normalized\EP',directory,fn))
        print directory

def combined_the_EP_subfactors():
    path=r'C:\data\barra_factors_normalized\EP'
    if not os.path.isdir(r'c:\data\barra_factors_combined\EP'):
        os.makedirs(r'c:\data\barra_factors_combined\EP')

    date_intersection=file_handler.get_date_intersection(path)

    directorys=os.listdir(path)
    for date in date_intersection:
        df=pd.DataFrame()
        for directory in directorys:
            sub_df=pd.read_csv(os.path.join(path,directory,'%s.csv'%date),index_col=0)
            df=df.append(sub_df)
        df=df.mean(axis=1)
        df=pd.DataFrame(df,columns=['EP'])
        df.to_csv(os.path.join(r'c:\data\barra_factors_combined\EP','%s.csv'%date))
        print date
#-----------------------------------------
#BP
def normalize_BP():
    directory=r'C:\data\barra_factors\PB'
    filenames=os.listdir(directory)
    for fn in filenames:
        df=pd.read_csv(os.path.join(directory,fn),index_col=0)
        df=1.0/df
        df=df_handler.normalize(df)
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\BP',fn))
        print fn

#----------------------------------------
#liquidity
def normalize_liquidity():
    path=r'C:\data\barra_factors\liquidity'
    date_intersection=file_handler.get_date_intersection(path)
    directorys=os.listdir(path)
    for date in date_intersection:
        for directory in directorys:
            tmp_df=pd.DataFrame()
            df=pd.read_csv(os.path.join(path,directory,date+'.csv'),index_col=0)
            df=np.log(df)
            df=df_handler.normalize(df)
            tmp_df=tmp_df.append(df)
            final_df=tmp_df.mean(axis=1)
            final_df=pd.DataFrame(final_df,columns=['liquidity'])
            final_df.to_csv(os.path.join(r'C:\data\barra_factors_combined\liquidity',date+'.csv'))
            print date

#----------------------------------------
#market value
def normalize_marketvalue():
    directory=r'C:\data\barra_factors\market_value'
    filenames=os.listdir(directory)
    for filename in filenames:
        df=pd.read_csv(os.path.join(directory,filename),index_col=0)
        df=np.log(df)
        df=df_handler.normalize(df)
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\market_value',filename))
        print filename

#----------------------------------------
#nls
def normalize_nls():
    directory=r'C:\data\barra_factors\nls'
    filenames=os.listdir(directory)
    for filename in filenames:
        df=pd.read_csv(os.path.join(directory,filename),index_col=0)
        df=df_handler.normalize(df)
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\nls',filename))
        print filename

#----------------------------------------
#beta
def normalize_beta():
    directory=r'C:\data\barra_factors\beta'
    filenames=os.listdir(directory)
    for filename in filenames:
        df=pd.read_csv(os.path.join(directory,filename),index_col=0)
        df=df_handler.normalize(df)
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\beta',filename))
        print filename

#----------------------------------------
#std_residual
def normalize_std_residual():
    directory = r'C:\data\barra_factors\std_residual'
    filenames = os.listdir(directory)
    for filename in filenames:
        df = pd.read_csv(os.path.join(directory, filename), index_col=0)
        df = df_handler.normalize(df)
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\std_residual', filename))
        print filename

#----------------------------------------
#momentum
def normalize_momentum():
    directory = r'C:\data\barra_factors\momentum'
    filenames = os.listdir(directory)
    for filename in filenames:
        df = pd.read_csv(os.path.join(directory, filename), index_col=0)
        df = df_handler.normalize(df)
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\momentum', filename))
        print filename

#-----------------------------------------
#reversion
def normalize_reversion():
    directory = r'C:\data\barra_factors\reversion'
    filenames = os.listdir(directory)
    for filename in filenames:
        df = pd.read_csv(os.path.join(directory, filename), index_col=0)
        df = df_handler.normalize(df)
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\reversion', filename))
        print filename




