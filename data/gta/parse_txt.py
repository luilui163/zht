# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-17  19:50
# NAME:zht-parse_txt.py

import os
import re
import pandas as pd
from multiprocessing import Pool
import time
from utils.dateu import get_current_time


dirpath=r'E:\a\gta20180412\unrars'
csvpath=r'E:\a\gta20180412\csv'

def txt2csv(fn):
    path=os.path.join(dirpath,fn)
    c=open(path,encoding='ISO-8859-1',newline='\r\n').read()
    '''
    By using notepad++ to show all the hiden character we can know that the line seperate is CRLF,that is,'\r\n'
    '''
    lines=c.split('\r\n')
    header=lines[0].split('\t')
    items=[]
    invalid=0
    for line in lines[3:-1]:
        #TODO: use regex to clear the data
        # l1=line.replace('\n','')
        # l2=re.sub('\t\t+', '\t', l1)
        # row=l2.split('\t')

        # line=line.replace('\n','')
        # line=re.sub('\t\t+','\t',line)

        row=line.split('\t')
        if len(row)==len(header):
            items.append(row)
        else:
            invalid+=1
    df=pd.DataFrame(items,columns=header)
    df.to_csv(os.path.join(csvpath,fn[:-4]+'.csv'),encoding='ISO-8859-1')
    print(get_current_time(),fn)
    return fn,len(lines)-3,invalid



if __name__=='__main__':
    fns = os.listdir(dirpath)
    sizes = [os.path.getsize(os.path.join(dirpath, fn)) for fn in fns]

    z = list(zip(fns, sizes))
    z = sorted(z, key=lambda x: x[1])
    fns=[a[0] for a in z]

    multi_fns=fns[:-50]
    single_fns=fns[-50:]

    p=Pool(4)
    items1=p.map(txt2csv,multi_fns)
    items2=[txt2csv(fn) for fn in single_fns]

    df=pd.DataFrame(items1+items2,columns=['fn','n','failed'])
    df.to_csv(r'e:\a\parse_result.csv')






