#-*-coding: utf-8 -*-
#@author:tyhj

import os
import pandas as pd
import numpy as np
from zht.data import data_handler

def get_date_intersection(path):
    directorys=os.listdir(path)
    date_intersection = []
    for i, directory in enumerate(directorys):
        file_names = os.listdir(os.path.join(path, directory))
        dates = [d[:10] for d in file_names]
        if i == 0:
            date_intersection = dates
        else:
            date_intersection = [d for d in date_intersection if d in dates]
    date_intersection.sort()
    return date_intersection

def growth():
    codes=data_handler.get_code_list()
    path=r'C:\data\cj\growth'
    date_intersection=get_date_intersection(path)
    directorys=os.listdir(path)
    # for directory in directorys:
    #     new_directory_path=os.path.join(r'C:\data\cj\final_data',directory)
    #     if not os.path.isdir(new_directory_path):
    #         os.makedirs(new_directory_path)
    for date in date_intersection:
        cross_df=pd.DataFrame()
        for directory in directorys:
            tmp_df=pd.read_csv(os.path.join(path,directory,date+'.csv'),index_col=0)
            cross_df=cross_df.append(tmp_df)
        cross_df=cross_df.dropna(axis=0)
        mean_df=cross_df.mean(axis=1)
        mean_df.to_csv(os.path.join(r'C:\data\cj\final_data\growth',date+'.csv'))
        print date


growth()







