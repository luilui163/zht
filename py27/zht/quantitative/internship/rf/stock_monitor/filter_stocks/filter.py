#-*-coding: utf-8 -*-
#@author:tyhj
import numpy as np
import pandas as pd



lines=open('jlr.txt').read().split('\n')[1:-1]
index=[l.split('\t')[0] for l in lines]
jlr1=[l.split('\t')[1] for l in lines]
jlr2=[l.split('\t')[2] for l in lines]
jlr_rate=[0.0]*len(jlr1)
for i in range(len(jlr1)):
    try:
        jlr_rate[i]=float(jlr2[i])/float(jlr1[i])-1
    except:
        jlr_rate[i]=np.NaN

df=pd.DataFrame(index=index)
df['jlr']=jlr_rate


lines=open('roe.txt').read().split('\n')[1:-1]
roe=[l.split('\t')[3] for l in lines]
for i in range(len(roe)):
    try:
        roe[i]=float(roe[i])
    except:
        roe[i]=np.NaN
df['roe']=roe


lines=open('yoygr.txt').read().split('\n')[1:-1]
yoygr=[l.split('\t')[2] for l in lines]
for i in range(len(yoygr)):
    try:
        yoygr[i]=float(yoygr[i])
    except:
        yoygr[i]=np.NaN
df['yoygr']=yoygr

lines=open('mv.txt').read().split('\n')[1:-1]
mv=[l.split('\t')[1] for l in lines]
for i in range(len(mv)):
    try:
        mv[i]=float(mv[i])
    except:
        mv[i]=np.NaN
df['mv']=mv


df=df[df['jlr']>0.3]
df=df[df['roe']>0.1]
df=df[df['yoygr']>0.3]
df=df[df['mv']<=40000000000]

df.to_csv('target_stocks.csv')










