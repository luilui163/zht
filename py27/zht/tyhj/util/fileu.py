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














