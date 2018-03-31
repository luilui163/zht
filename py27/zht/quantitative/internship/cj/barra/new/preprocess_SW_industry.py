#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
import os
from tool import mark

def _statistic_SW_industry():
    path=r'C:\data\barra_factors\industry'
    filenames=os.listdir(path)
    value_counts=pd.DataFrame()
    for filename in filenames:
        df=pd.read_csv(os.path.join(path,filename),index_col=0)
        ct=df.iloc[:,0].value_counts()
        value_counts[filename[:-4]]=ct
    value_counts=value_counts.T
    value_counts.to_csv(r'C:\data\derivative_factors\SW_fistclass_industry_stats.csv')
    return value_counts

def _get_industry_intersection():
    '''
    Since in different month_ends there is different industry classes.
    After taking intersection,there is only 15 industrys
    '''
    path=r'C:\data\barra_factors\industry'
    filenames=os.listdir(path)
    df = pd.read_csv(os.path.join(path, filenames[0]), index_col=0)
    ct = df.iloc[:, 0].unique()
    industry_intersection=set(ct)
    for filename in filenames[1:]:
        df=pd.read_csv(os.path.join(path,filename),index_col=0)
        ct = df.iloc[:, 0].unique()
        industry_intersection=industry_intersection.intersection(set(ct))
    industry_intersection=list(industry_intersection)
    return industry_intersection

@mark
def change_the_industry_format():
    if not os.path.isdir(r'c:\data\barra_factors_combined\industry'):
        os.makedirs(r'c:\data\barra_factors_combined\industry')
    industry_intersection = _get_industry_intersection()
    path = r'C:\data\barra_factors\industry'
    filenames = os.listdir(path)
    for filename in filenames:
        df=pd.read_csv(os.path.join(path,filename),index_col=0)
        #change industry name
        df=df.applymap(lambda x:'SW_'+str(int(x)) if x in industry_intersection else 'SW_other')
        #change the format of the industry df
        df1=pd.DataFrame()
        s = df.iloc[:,0]
        d=dict(s)
        for code in d:
            df1.loc[code,d[code]]=1
        df[df=='other']=0 #the dummy variable should be larger than the number of industry by 1
        df1=df1.fillna(0)
        df1.to_csv(os.path.join(r'C:\data\barra_factors_combined\industry',filename))
        print 'change_the_industry_format',filename

#TODO:to recollect the industry data
if __name__=='__main__':
    change_the_industry_format()


