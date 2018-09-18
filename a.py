# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-08-27  21:42
# NAME:FT_hp-a.py

import os
import pandas as pd
# import copy

import numpy as np


dirpath=r'E:\a\a'
csvpath=r'e:\a\csv1'



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
    for line in lines[1:-1]:
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
    print(len(lines)-3,invalid)
    return fn,len(lines)-3,invalid

def parse_all():
    fns=os.listdir(dirpath)
    for fn in fns:
        txt2csv(fn)
        print(fn)

def select_base_variables():
    fns=os.listdir(csvpath)
    ss=[]
    for fn in fns:
        df=pd.read_csv(os.path.join(csvpath,fn),index_col=0,encoding='gbk')
        s=df.iloc[0,:]
        ss.append(s)

    df=pd.concat(ss,axis=0,keys=[fn[:-4] for fn in fns])
    df=df.to_frame().reset_index()
    df.head()
    df.columns=['sname','indicator','name']

    df.to_csv(r'e:\a\df.csv',encoding='gbk')


# if __name__ == '__main__':
#     parse_all()
