#-*-coding: utf-8 -*-
#@author:tyhj

import multiprocessing
import time
from utils.listu import chunkify


def mark(func):
    def wrapped():
        func()
        print(func.__name__,'finished')
    return wrapped

def monitor(func):

    def wrapper(*args,**kwargs):
        print('{}   starting -> {}'.format(time.strftime('%Y-%m-%d %H:%M:%S'),func.__name__))
        return func(*args,**kwargs)

    return wrapper


def multiProcess(func,args,multiNum=4):
    '''
    multiprocessing

    note:
        the multiprocessing can only run in the __name__=='__main__' condition

    Args:
        func:
        args: list or tuple,and the element in the
        multiNum:

    Returns:

    '''
    jobs=[]
    argList=chunkify(args,multiNum)
    for i in range(multiNum):
        p=multiprocessing.Process(target=func,args=(argList[i],))
        jobs.append(p)
        p.start()









