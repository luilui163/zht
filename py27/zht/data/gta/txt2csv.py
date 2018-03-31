#-*-coding: utf-8 -*-
#author:tyhj
#txt2csv.py 2017/7/31 10:59

import os
import pandas as pd


def toDf():
    dirpath=r'E:\GTA\txt'#TODO:
    tablesPath=r'D:\quantDb\sourceData\gta\data\tables'
    fns=[fn for fn in os.listdir(dirpath) if fn.endswith('.txt')][800:1500]#TODO:

    wrongFiles=[]
    for i,fn in enumerate(fns):
        try:
            print i,fn
            path=os.path.join(dirpath,fn)
            c=open(path).read()

            c=c.replace('\n\t','')
            c=c.replace('\n\t','')
            c=c.replace('\n\r','')
            c=c.replace('\n\r','')
            c=c.replace('\r','')
            c=c.replace(' ','')
            # df=pd.read_csv(path,index_col=0,sep='\t')
            # df.to_csv(r'e:\aa\txt\df1.csv')
            header=c.split('\n')[0].split('\t')
            name=c.split('\n')[1].split('\t')
            unit=c.split('\n')[2].split('\t')

            df=pd.DataFrame([l.split('\t') for l in c.split('\n') if len(l.split('\t'))==len(header)][3:],columns=header)
            df=df.set_index(header[0])
            df.to_csv(r'E:\GTA\csv\%s.csv'%fn[:-4])#TODO
        except:
            wrongFiles.append('fn')

def txt2csv(fp):
    name=os.path.basename(fp)[:-4]
    c = open(fp).read()

    c = c.replace('\n\t', '')
    c = c.replace('\n\t', '')
    c = c.replace('\n\r', '')
    c = c.replace('\n\r', '')
    c = c.replace('\r', '')
    c = c.replace(' ', '')
    # df=pd.read_csv(path,index_col=0,sep='\t')
    # df.to_csv(r'e:\aa\txt\df1.csv')
    header = c.split('\n')[0].split('\t')
    # name = c.split('\n')[1].split('\t')
    # unit = c.split('\n')[2].split('\t')

    df = pd.DataFrame([l.split('\t') for l in c.split('\n') if len(l.split('\t')) == len(header)][3:], columns=header)
    df = df.set_index(header[0])
    df.to_csv(r'E:\GTA\csv\%s.csv' % name)  # TODO


dirpath1=r'E:\GTA\txt'
dirpath2=r'E:\GTA\csv'

fns1=os.listdir(dirpath1)
fns2=os.listdir(dirpath2)
names1=[fn[:-4] for fn in fns1]
names2=[fn[:-4] for fn in fns2]
fns=[fn for fn in fns1 if fn[:-4] not in names2]
fns=sorted(fns,key=lambda fn:os.path.getsize(os.path.join(dirpath1,fn)))

with open('log.txt','w') as f:
    for i,fn in enumerate(fns):
        f.write('%s\t%s\n'%(i,fn))
        print i,fn
        fp=os.path.join(dirpath1,fn)
        txt2csv(fp)
#TODO:there are still some files too large to handle






fp=r'E:\GTA\txt\STK_MKT_StyleBox.txt'
tmppath=r'e:\aa\tmp.txt'

c = open(fp).read()
c = c.replace('\n\t', '')
c = c.replace('\n\t', '')
c = c.replace('\n\r', '')
c = c.replace('\n\r', '')
c = c.replace('\r', '')
c = c.replace(' ', '')

header = c.split('\n')[0].split('\t')
width=len(header)
with open(tmppath,'w') as f:
    f.write(c)

del c# since c is too large,delete it to save memory

items=[]
with open(tmppath) as f:
    for line in f:
        if len(line.split('\t'))==width:
            items.append(line.split('\t'))

df = pd.DataFrame(items[3:], columns=header)
df = df.set_index(header[0])
df.to_csv(r'e:\aa\csv.csv')


df=pd.read_csv(tmppath,sep='\t')
df=df[2:]

# import sys
# print sys.getsizeof(df)
