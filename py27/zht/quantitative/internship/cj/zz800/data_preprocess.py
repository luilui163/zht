#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import os

#得到不同文件夹下所共有的同日期的文件名
def get_intersection_filenames(paths):
    filenames_list=[]
    for path in paths:
        filenames=os.listdir(path)
        filenames_list.append(filenames)
    intersection_filenames=reduce(lambda x,y:list(set(x).intersection(set(y))),filenames_list)
    intersection_filenames=sorted(intersection_filenames)
    return intersection_filenames







