# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 13:48:20 2016

@author: Administrator
"""
import pandas as pd
import time

start=time.time()
number=50#选择最先发布和最后发布的股票的个数
length=10#收益考察天数


marketAdjustedReturnDF=pd.read_csv(r'c:\marketAdjustedReturnDF_2004-2016.csv',index_col=0)
stock1=[s for s in marketAdjustedReturnDF.columns]

path=r'c:\earning_calendar\quarter\2012Q4.txt'
line=open(path).read().split('\n')[:-1]
date=[]
stock=[]
for i in range(len(line)):
    if line[i].split('\t')[1] in stock1:
        date.append(int(line[i].split('\t')[0]))
        stock.append(line[i].split('\t')[1])
DFtmp=pd.DataFrame({'stock':stock},index=date)
DFsorted=DFtmp.sort_index()
DFearly=DFsorted.iloc[:number]
DFlate=DFsorted.iloc[-number:]
dateList=[d for d in marketAdjustedReturnDF.index]



####test early stocks
earlyave1=['']*len(DFearly)
earlyave2=['']*len(DFearly)
for k1 in range(len(DFearly)):
    for m1 in range(len(dateList)):
        if dateList[m1]-DFearly.index[k1]<0 and dateList[m1+1]-DFearly.index[k1]>=0:
            earlybeforeIndex2=m1+1
            break
    earlybeforeIndex1=earlybeforeIndex2-length
#找到年报发布后的第一个开盘数据
    for n1 in range(earlybeforeIndex2,len(dateList)):
        col=[c for c in marketAdjustedReturnDF.columns]
        colIndex=col.index(DFearly.iat[k1,0])
        if str(marketAdjustedReturnDF.iat[n1,colIndex])!='nan':
            earlyafterIndex1=n1
            break
#    afterIndex1=beforeIndex2+1
    earlyafterIndex2=earlyafterIndex1+length
#    afterIndex1=beforeIndex2
#    afterIndex2=afterIndex1+length
    earlyTmpDF1=marketAdjustedReturnDF[DFearly.iat[k1,0]].iloc[earlybeforeIndex1:earlybeforeIndex2]
    earlyTmpDF2=marketAdjustedReturnDF[DFearly.iat[k1,0]].iloc[earlyafterIndex1:earlyafterIndex2]
    earlyave1[k1]=earlyTmpDF1.mean()
    earlyave2[k1]=earlyTmpDF2.mean()
earlycount1=0
earlycount2=0
earlysum1=0
earlysum2=0
for q in range(len(earlyave1)):
    if str(earlyave1[q])!='nan':#######注意list中的nan是float型，所以先用str转化类型，再判断
        earlycount1+=1
        earlysum1=earlysum1+earlyave1[q]
    if str(earlyave2[q])!='nan':
        earlycount2+=1
        earlysum2=earlysum2+earlyave2[q]
earlybeforeReturn=earlysum1/earlycount1
earlyafterReturn=earlysum2/earlycount2




######test late stocks
lateave1=['']*len(DFlate)
lateave2=['']*len(DFlate)
for k2 in range(len(DFlate)):
    for m2 in range(len(dateList)):
        if dateList[m2]-DFlate.index[k2]<0 and dateList[m2+1]-DFlate.index[k2]>=0:
            latebeforeIndex2=m2+1
            break
    latebeforeIndex1=latebeforeIndex2-length
#找到年报发布后的第一个开盘数据
    for n2 in range(latebeforeIndex2,len(dateList)):
        col=[c for c in marketAdjustedReturnDF.columns]
        colIndex=col.index(DFearly.iat[k2,0])
        if str(marketAdjustedReturnDF.iat[n2,colIndex])!='nan':
            lateafterIndex1=n2
            break
#    afterIndex1=beforeIndex2+1
    lateafterIndex2=lateafterIndex1+length
#    afterIndex1=beforeIndex2
#    afterIndex2=afterIndex1+length
    lateTmpDF1=marketAdjustedReturnDF[DFearly.iat[k2,0]].iloc[latebeforeIndex1:latebeforeIndex2]
    lateTmpDF2=marketAdjustedReturnDF[DFearly.iat[k2,0]].iloc[lateafterIndex1:lateafterIndex2]
    lateave1[k2]=lateTmpDF1.mean()
    lateave2[k2]=lateTmpDF2.mean()
latecount1=0
latecount2=0
latesum1=0
latesum2=0
for q in range(len(lateave1)):
    if str(lateave1[q])!='nan':#######注意list中的nan是float型，所以先用str转化类型，再判断
        latecount1+=1
        latesum1=latesum1+lateave1[q]
    if str(lateave2[q])!='nan':
        latecount2+=1
        latesum2=latesum2+lateave2[q]
latebeforeReturn=latesum1/latecount1
lateafterReturn=latesum2/latecount2

print 'number=',number,'length=',length,'early',earlyafterReturn,earlybeforeReturn,earlyafterReturn-earlybeforeReturn
print 'number=',number,'length=',length,'late',lateafterReturn,latebeforeReturn,lateafterReturn-latebeforeReturn

end=time.time()
print end-start
    

    
    
    
    
    
    