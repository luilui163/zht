#-*-coding: utf-8 -*-
#@author:tyhj

import os
import pandas as pd
import numpy as np
from zht.data import file_handler
from tool import mark,normalize
import shutil

#-----------------------------------------
#growth
#TODO: 计算growth值时候，少了一个子类研报中有三个指标合成，但是这里只有两个,wind一直预期净利润增速数据太少，没有使用，所以只有两个subfactor

def _prepare_growth():
    for dirpath,dirnames,filenames in os.walk(r'C:\data\barra_factors_normalized\growth'):
        for filename in filenames:
            os.remove(os.path.join(dirpath,filename))

    path=r'C:\data\barra_factors\growth'
    directorys=os.listdir(path)
    for directory in directorys:
        if not os.path.isdir(os.path.join(r'C:\data\barra_factors_normalized\growth',directory)):
            os.makedirs(os.path.join(r'C:\data\barra_factors_normalized\growth',directory))

        filenames=os.listdir(os.path.join(path,directory))
        for filename in filenames:
            df=pd.read_csv(os.path.join(path,directory,filename),index_col=0)
            df=normalize(df,filename[:-4])
            # df=(df-df.mean())/df.std()
            df.to_csv(os.path.join(r'C:\data\barra_factors_normalized\growth',directory,filename))
        print directory

@mark
def _normalize_growth():
    _prepare_growth()

    path=r'C:\data\barra_factors_normalized\growth'
    #some of the filenames do not correspond with each other
    if not os.path.isdir(r'c:\data\barra_factors_combined\growth'):
        os.makedirs(r'c:\data\barra_factors_combined\growth')

    date_intersection=file_handler.get_date_intersection(path)
    directorys=os.listdir(path)
    for date in date_intersection:
        df=pd.DataFrame()
        for directory in directorys:
            sub_df=pd.read_csv(os.path.join(path,directory,'%s.csv'%date),index_col=0)
            df[directory]=sub_df.iloc[:,0]
        s=df.mean(axis=1)
        df=pd.DataFrame(s,columns=['growth'])
        df.to_csv(os.path.join(r'c:\data\barra_factors_combined\growth','%s.csv'%date))

#-----------------------------------------
#EP
def _prepare_EP():
    for dirpath,dirnames,filenames in os.walk(r'C:\data\barra_factors_normalized\EP'):
        for filename in filenames:
            os.remove(os.path.join(dirpath,filename))

    path=r'C:\data\barra_factors\EP'
    directorys=os.listdir(path)
    for directory in directorys:
        if not os.path.isdir(os.path.join(r'C:\data\barra_factors_normalized\EP',directory)):
            os.makedirs(os.path.join(r'C:\data\barra_factors_normalized\EP',directory))

        filenames=os.listdir(os.path.join(path,directory))
        for fn in filenames:
            df=pd.read_csv(os.path.join(path,directory,fn),index_col=0)
            df=1/df  #since the initial df is PE,we need to get EP
            df = normalize(df, fn[:-4])
            # df = (df - df.mean()) / df.std()
            df.to_csv(os.path.join(r'C:\data\barra_factors_normalized\EP',directory,fn))

@mark
def _normalize_EP():
    _prepare_EP()
    path=r'C:\data\barra_factors_normalized\EP'
    # some of the filenames do not correspond with each other
    if not os.path.isdir(r'c:\data\barra_factors_combined\EP'):
        os.makedirs(r'c:\data\barra_factors_combined\EP')

    date_intersection=file_handler.get_date_intersection(path)
    directorys=os.listdir(path)
    for date in date_intersection:
        df=pd.DataFrame()
        for directory in directorys:
            sub_df=pd.read_csv(os.path.join(path,directory,'%s.csv'%date),index_col=0)
            df[directory]=sub_df.iloc[:,0]
        s=df.mean(axis=1)
        df=pd.DataFrame(s,columns=['EP'])
        df.to_csv(os.path.join(r'c:\data\barra_factors_combined\EP','%s.csv'%date))

#-----------------------------------------
#BP
@mark
def _normalize_BP():
    if not os.path.isdir(r'c:\data\barra_factors_combined\BP'):
        os.makedirs(r'c:\data\barra_factors_combined\BP')

    directory=r'C:\data\barra_factors\PB'
    filenames=os.listdir(directory)
    for filename in filenames:
        df=pd.read_csv(os.path.join(directory,filename),index_col=0)
        df=1.0/df
        df = normalize(df, filename[:-4])
        # df = (df - df.mean()) / df.std()
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\BP',filename))

#----------------------------------------
#liquidity
@mark
def _normalize_liquidity():
    if not os.path.isdir(r'c:\data\barra_factors_combined\liquidity'):
        os.makedirs(r'c:\data\barra_factors_combined\liquidity')
    path=r'C:\data\barra_factors\liquidity'
    date_intersection=file_handler.get_date_intersection(path)
    directorys=os.listdir(path)
    for date in date_intersection:
        df=pd.DataFrame()
        for directory in directorys:
            sub_df=pd.read_csv(os.path.join(path,directory,date+'.csv'),index_col=0)
            sub_df=np.log(sub_df)
            sub_df= normalize(sub_df, date)
            df[directory]=sub_df.iloc[:,0]
        s=df.mean(axis=1)
        final_df=pd.DataFrame(s,columns=['liquidity'])
        # final_df = (final_df - final_df.mean()) / final_df.std()
        final_df.to_csv(os.path.join(r'C:\data\barra_factors_combined\liquidity',date+'.csv'))

#----------------------------------------
#market value
@mark
def _normalize_market_value():
    if not os.path.isdir(r'c:\data\barra_factors_combined\market_value'):
        os.makedirs(r'c:\data\barra_factors_combined\market_value')
    directory=r'C:\data\barra_factors\market_value'
    filenames=os.listdir(directory)
    for filename in filenames:
        df=pd.read_csv(os.path.join(directory,filename),index_col=0)
        df=np.log(df)
        df = normalize(df, filename[:-4])
        # df = (df - df.mean()) / df.std()
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\market_value',filename))

#----------------------------------------
#nls
@mark
def _normalize_nls():
    if not os.path.isdir(r'c:\data\barra_factors_combined\nls'):
        os.makedirs(r'c:\data\barra_factors_combined\nls')
    directory=r'C:\data\barra_factors\nls'
    filenames=os.listdir(directory)
    for filename in filenames:
        df=pd.read_csv(os.path.join(directory,filename),index_col=0)
        df = normalize(df, filename[:-4])
        # df = (df - df.mean()) / df.std()
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\nls',filename))

#----------------------------------------
#beta
@mark
def _normalize_beta():
    if not os.path.isdir(r'c:\data\barra_factors_combined\beta'):
        os.makedirs(r'c:\data\barra_factors_combined\beta')
    directory=r'C:\data\barra_factors\beta'
    filenames=os.listdir(directory)
    for filename in filenames:
        df=pd.read_csv(os.path.join(directory,filename),index_col=0)
        df = normalize(df, filename[:-4])
        # df = (df - df.mean()) / df.std()
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\beta',filename))

#----------------------------------------
#std_residual
@mark
def _normalize_std_residual():
    if not os.path.isdir(r'c:\data\barra_factors_combined\std_residual'):
        os.makedirs(r'c:\data\barra_factors_combined\std_residual')
    directory = r'C:\data\barra_factors\std_residual'
    filenames = os.listdir(directory)
    for filename in filenames:
        df = pd.read_csv(os.path.join(directory, filename), index_col=0)
        df = normalize(df, filename[:-4])
        # df = (df - df.mean()) / df.std()
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\std_residual', filename))

#----------------------------------------
#momentum
@mark
def _normalize_momentum():
    if not os.path.isdir(r'c:\data\barra_factors_combined\momentum'):
        os.makedirs(r'c:\data\barra_factors_combined\momentum')
    directory = r'C:\data\barra_factors\momentum'
    filenames = os.listdir(directory)
    for filename in filenames:
        df = pd.read_csv(os.path.join(directory, filename), index_col=0)
        df = normalize(df, filename[:-4])
        # df = (df - df.mean()) / df.std()
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\momentum', filename))

#-----------------------------------------
#reversion
@mark
def _normalize_reversion():
    if not os.path.isdir(r'c:\data\barra_factors_combined\reversion'):
        os.makedirs(r'c:\data\barra_factors_combined\reversion')
    directory = r'C:\data\barra_factors\reversion'
    filenames = os.listdir(directory)
    for filename in filenames:
        df = pd.read_csv(os.path.join(directory, filename), index_col=0)
        df = normalize(df, filename[:-4])
        # df = (df - df.mean()) / df.std()
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\reversion', filename))

#------------------------------------------
#weithts
@mark
def _get_weights():
    if not os.path.isdir(r'c:\data\barra_factors_combined\weights'):
        os.makedirs(r'c:\data\barra_factors_combined\weights')
    directory=r'C:\data\barra_factors\market_value'
    filenames=os.listdir(directory)
    for filename in filenames:
        df=pd.read_csv(os.path.join(directory,filename),index_col=0)
        df=np.sqrt(df)
        # df=1000/df #the weights in WLS are inversely to the square root of the market capitalization
        df.to_csv(os.path.join(r'C:\data\barra_factors_combined\weights',filename))

@mark
def _get_size():
    src=r'c:\data\barra_factors\market_value'
    dst=r'c:\data\barra_factors_combined\size'
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src,dst)

def run():
    _normalize_growth()
    _normalize_EP()
    _normalize_BP()
    _normalize_liquidity()
    _normalize_market_value()
    _normalize_nls()
    _normalize_beta()
    _normalize_std_residual()
    _normalize_momentum()
    _normalize_reversion()
    _get_weights()
    _get_size()


if __name__ == '__main__':
    run()



