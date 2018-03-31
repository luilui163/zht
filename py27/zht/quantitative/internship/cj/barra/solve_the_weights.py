#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
from zht.data import data_handler
import os

'''
the returns of stock in the left hand of the regression equation should be
adjusted by risk free return.
'''
rf=0.03/12


#TODO:How to deal with the NaN? Using dropna(axis=0,how='any') will reduce the samples remarkedly
#TODO:how to add weights? add the weights before droping NaN or after droping NaN
def get_cross_sectional_df():
    directory=r'C:\data\gx\csvdata\normalized_factors'
    file_names=os.listdir(directory)
    file_names=[fn for fn in file_names if fn[-5]!='1']
    #get the intersection date for these df
    start_date='2001-01-01'
    end_date='2100-01-01'
    for fn in file_names:
        date1=pd.read_csv(os.path.join(directory,fn),index_col=0).index[0]
        date2= pd.read_csv(os.path.join(directory, fn), index_col=0).index[-1]
        if date1>start_date:
            start_date=date1
        if date2<end_date:
            end_date=date2
    month_ends=pd.date_range(start_date,end_date,freq='M')

    for month_end in month_ends:
        month_end=month_end.strftime('%Y-%m-%d')
        cross_sectional_df=pd.DataFrame()
        for fn in file_names:
            row_for_one_factor=pd.read_csv(os.path.join(directory,fn),index_col=0).loc[month_end]
            factor_name=fn[:-4]
            cross_sectional_df[factor_name]=row_for_one_factor
            cross_sectional_df['weight']=1 #TODO: add the weights by using the square root of market size
        cross_sectional_df.to_csv(r'C:\data\gx\csvdata\cross_sectional_data\%s.csv'%month_end)
        print month_end

# get_cross_sectional_df()

directory=r'C:\data\gx\csvdata\cross_sectional_data'
file_names=os.listdir(directory)
fn=file_names[-1]
df=pd.read_csv(os.path.join(directory,fn),index_col=0)



print len(df)
df=df.dropna(axis=0,how='any')
print len(df)


factor_names=[f for f in df.columns if f!='weight']
X=np.matrix(df[factor_names])
W=np.diag(df['weight'])

pure_factor_weights_for_stock=(X.T*W*X).getI()*X.T*W

factor_weights_df=pd.DataFrame(pure_factor_weights_for_stock.T,index=df.index,columns=factor_names)










