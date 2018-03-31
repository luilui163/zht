#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
import numpy as np
import os
from scipy.stats import mstats


#hamdle the outliers
def handle_outliers1(df):
    # method 1,the largest and smallest quantile are delete
    new_df=pd.DataFrame(index=df.index)
    for code in df.columns:
        data=df[code]
        data[data>np.percentile(data,95)]=np.percentile(data,90)
        data[data<np.percentile(data,5)]=np.percentile(data,5)
        new_df[code]=data
    return new_df

def handle_outliers2(df):
    #method 2,using 3 std as the threshhold
    new_df=pd.DataFrame(index=df.index)
    for code in df.columns:
        data=df[code]
        data[data-data.mean()<-3*data.std()]=data.mean()-3*data.std()
        data[data-data.mean()>3*data.std()]=data.mean()+3*data.std()
        new_df[code]=data
    return new_df

def handle_outliers3(df,m=3):
    #median
    for code in df.columns:
        data=df[code]
        d=np.abs(data-np.median(data))
        mdev=np.median(d)
        for i in range(len(df[code])):
            s=df[code][i]/mdev if mdev else 0
            if s>m:
                print s
                df[code][i]=np.NaN
    return df

def normalize(df):
    #using the method 2
    df=handle_outliers2(df)
    normalized_df=(df-df.mean())/df.std()
    return normalized_df

def run():
    file_path=r'C:\data\gx\csvdata\factors'
    file_names=os.listdir(file_path)
    for fn in file_names:
        df=pd.read_csv(os.path.join(file_path,fn),index_col=0)
        df=normalize(df)
        df.to_csv(r'C:\data\gx\csvdata\normalized_factors\%s'%fn)
        print fn

def run2():
    path=r'C:\data\factors'
    directorys=os.listdir(path)
    for directory in directorys:
        new_dir_path=os.path.join(r'C:\data\normalized_factors',directory)
        if not os.path.isdir(new_dir_path):
            os.makedirs(new_dir_path)
        filenames=os.listdir(os.path.join(path,directory))
        for fn in filenames:
            df=pd.read_csv(os.path.join(path,directory,fn),index_col=0)
            df=normalize(df)
            df.to_csv(os.path.join(new_dir_path,fn))
        print directory



if __name__=='__main__':
    run2()






