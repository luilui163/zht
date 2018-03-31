#-*-coding: utf-8 -*-
#@author:tyhj

import os


def get_date_intersection(directory):
    '''
    :param directory: the target directory in which there are several
    subdirectorys
    :return: the date_intersection in these subdirectory,in list type
    '''
    factor_names=os.listdir(directory)

    date_intersection=[]
    for i,fn in enumerate(factor_names):
        file_names=os.listdir(os.path.join(directory,fn))
        dates=[fn[:10] for fn in file_names]
        if i == 0:
            date_intersection=dates
        else:
            date_intersection=[d for d in date_intersection if d in dates]
    return date_intersection












