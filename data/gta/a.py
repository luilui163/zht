# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-18  00:20
# NAME:zht-a.py
import os
from multiprocessing.pool import Pool

import pandas as pd
from utils.dateu import get_current_time

txtDir= r'E:\a\gta20180412\txt'
txtNewDir=r'E:\a\gta20180412\txtNew'
csvDir= r'E:\a\gta20180412\csv'

def clean_txt(fn):
    inputPath=os.path.join(txtDir, fn)
    outputPath=os.path.join(txtNewDir, fn)
    bunchsize=1000000
    valid=0
    invalid=0
    bunch=[]
    with open(inputPath,encoding='ISO-8859-1',newline='\r\n') as r,\
            open(outputPath,'w',encoding='ISO-8859-1') as w:
        coln=len(r.readline().split('\t'))
        for line in r:
            if len(line.split('\t'))==coln:
                # bunch.append(line+'\n') #'\n` denote CRLF in python3
                # bunch.append(line.replace('\n','').replace(' ','')) #'\n` denote CRLF in python3
                # newline=line.replace('\n','').replace(' ','').replace(',','').replace('\t',',')
                newline=line.replace('\n','').replace(' ','')
                bunch.append(newline)
                valid+=1
            else:
                invalid+=1

            if len(bunch)==bunchsize:
                # w.write(l+'\r\n' for l in bunch)
                w.writelines(bunch) #equals w.write(l+'\n' for l in bunch)
                bunch=[]

        w.writelines(bunch)

    print(fn)
    return fn,valid,invalid



def txt2csv(fn):
    fp=os.path.join(txtNewDir,fn+'.txt')
    df = pd.DataFrame([row.split('\t') for row in open(fp, encoding='ISO-8859-1', newline='\r').readlines()])
    df.to_csv(os.path.join(csvDir, fn+'.csv'))

if __name__=='__main__':
    fns = os.listdir(txtDir)
    p=Pool(10)
    items=p.map(clean_txt, fns)

    df=pd.DataFrame(items, columns=['fn', 'valid', 'invalid'])
    df['ratio']=df['invalid']/(df['valid']+df['invalid'])
    df=df.sort_values('ratio',ascending=False)
    df.to_csv(r'E:\a\gta20180412\invalid_ratio.csv')


    #
    # with open(r'e:\a\log.txt','w') as log:
    #     # log.write('\n'.join([','.join(item) for item in items]))
    #
    #     for i,fn in enumerate(single_fns):
    #         log.write('{},{},{}'.format(*clean_txt(fn[:-4])))
    #         print(get_current_time(),i,fn)
