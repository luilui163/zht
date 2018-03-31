#-*-coding: utf-8 -*-
#@author:tyhj
import os
import time
import datetime



def getModificationTime(filePath):
    '''
    return the modification of a file
    :param filePath: str
    :return: datetime
    '''
    mtime=os.stat(filePath).st_mtime
    mtime=time.localtime(mtime)
    mtimeDate=datetime.datetime(*mtime[:6])
    return mtimeDate

#获取两个文件夹下文件名的交集
def get_intersection_filenames1(dirpath1,dirpath2):
    filenames1=os.listdir(dirpath1)
    filenames2=os.listdir(dirpath2)
    intersection=set(filenames1).intersection(set(filenames2))
    intersection=sorted(list(intersection))
    return intersection


def get_intersection_filenames2(dirpath):
    '''
    there are several subdirectorys in dirpath,return the intersection
    '''
    factornames = os.listdir(dirpath)
    filenames_intersection=[]
    for i,fn in enumerate(factornames):
        filenames=os.listdir(os.path.join(dirpath,fn))
        if i == 0:
            filenames_intersection=filenames
        else:
            filenames_intersection=[d for d in filenames_intersection if d in filenames]
    return filenames_intersection














