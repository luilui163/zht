#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import os
from zht.data import file_handler
import calendar
import numpy as np
from tool import mark
import shutil
import time

@mark
def run():
    #remove the old files
    if os.path.exists(r'c:\data\barra_cross_data'):
        shutil.rmtree(r'C:\data\barra_cross_data')
    time.sleep(1)
    os.makedirs(r'c:\data\barra_cross_data')
    #setting the risk free return as 0.04
    risk_free=0.04/12 #TODO:which risk free to choose?
    # risk_free=0
    path = r'C:\data\barra_factors_combined'
    date_intersection=file_handler.get_date_intersection(path)
    directorys = os.listdir(path)
    for i in range(1,len(date_intersection)):
        cross_df=pd.DataFrame()
        for directory in directorys:
            if directory!='month_returns':
                #since in time T,we use the factors in T-1 to regress the equation
                df=pd.read_csv(os.path.join(path,directory,date_intersection[i-1]+'.csv'),index_col=0)
            else:
                df = pd.read_csv(os.path.join(path, directory, date_intersection[i] + '.csv'), index_col=0)
                df=df-risk_free

            if directory=='industry':
                cross_df=pd.concat([cross_df,df],axis=1) #or using .merge
            else:
                cross_df[directory]=df.iloc[:,0]
        cross_df['fc']=1 #add a intercept to the regression equation
        cross_df=cross_df.drop(cross_df[pd.isnull(cross_df['weights'])].index)# drop those tick with null in weights
        cross_df=cross_df.dropna(axis=0,thresh=len(cross_df.columns)-2)
        cross_df=cross_df.fillna(0)
        # cross_df=cross_df.dropna(axis=0)
        cross_df.to_csv(os.path.join(r'C:\data\barra_cross_data',date_intersection[i]+'.csv'))



if __name__=='__main__':
    run()




