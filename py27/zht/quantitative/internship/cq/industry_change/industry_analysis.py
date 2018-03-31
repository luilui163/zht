# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 13:48:20 2016

@author: Administrator
"""
import time
import pandas as pd
import numpy as np

start=time.time()


returnDF=pd.read_csv(r'c:\residualReturnDF.csv',index_col=0)


classificationPath=r'd:\classification\SW.txt'

def getDifferenceStock(classificationPath,returnDF):
    line=open(classificationPath).read().split('\n')
    stockList=['']*(len(line)-1)
    classification=['']*(len(line)-1)
    for i in range(len(line)-1):
        stockList[i]=line[i].split('\t')[0]
        classification[i]=line[i].split('\t')[1]
    list2=[m for m in returnDF.columns]
    differenceStock1=[stock for stock in list2 if stock not in stockList]
    differenceStock2=[stock for stock in stockList if stock not in list2]
    for j in range(len(differenceStock2)):
        del classification[stockList.index(differenceStock2[j])]
        stockList.remove(differenceStock2[j])
    return (stockList,classification,differenceStock1)
    
(stockList,classification,differenceStock)=getDifferenceStock(classificationPath,returnDF)

def getIntersectionCorrDF(returnDF,differenceStock):
    intersectionReturnDF=returnDF
    for i in range(len(differenceStock)):
        del intersectionReturnDF[differenceStock[i]]
    
    return intersectionReturnDF
    
intersectionReturnDF=getIntersectionCorrDF(returnDF,differenceStock)
m=intersectionReturnDF.T

def getStd(m,stockList,classification):
    intersectionReturnDF[intersectionReturnDF>0.11]=0
    intersectionReturnDF[intersectionReturnDF<-0.11]=0
    category=sorted(list(set(classification)))
    classificationDF=pd.DataFrame(classification,index=stockList,columns=['classification'])
    newReturnDF=pd.concat([classificationDF,m],axis=1)
    std=[0]*len(category)
    for i in range(len(category)):
        tmpDF=newReturnDF[newReturnDF['classification'].isin([category[i]])]
        tmpDF=tmpDF.fillna(value=0)
        averageR=[0]*(len(tmpDF.T)-2)
        for m in range(2,len(tmpDF.T)):
            count=0
            total=0
            for n in range(len(tmpDF)):
                if tmpDF.iat[n,m]!=0:
#                    print n,m,tmpDF.iat[n,m]
                    count+=1
                    total=total+tmpDF.iat[n,m]
            if count==0:
                averageR[m]=0
            else:
                averageR[m-2]=total/count
        arr=np.array(averageR)
        std[i]=np.std(arr)
    return std
std=getStd(m,stockList,classification)








corrDF=pd.read_csv(r'c:\residualReturnCorr.csv',index_col=0)

def getDifferenceStock(classificationPath,corrDF):
    line=open(classificationPath).read().split('\n')
    stockList=['']*(len(line)-1)
    classification=['']*(len(line)-1)
    for i in range(len(line)-1):
        stockList[i]=line[i].split('\t')[0]
        classification[i]=line[i].split('\t')[1]
    list2=[m for m in corrDF.index]
    differenceStock1=[stock for stock in list2 if stock not in stockList]
    differenceStock2=[stock for stock in stockList if stock not in list2]
    for j in range(len(differenceStock2)):
        del classification[stockList.index(differenceStock2[j])]
        stockList.remove(differenceStock2[j])
    return (stockList,classification,differenceStock1)
    

(stockList,classification,differenceStock)=getDifferenceStock(classificationPath,corrDF)

def getIntersectionCorrDF(corrDF,differenceStock):
    intersectionCorrDF=corrDF
    for i in range(len(differenceStock)):
        intersectionCorrDF=intersectionCorrDF.drop(differenceStock[i])
        del intersectionCorrDF[differenceStock[i]]
    return intersectionCorrDF
    
intersectionCorrDF=getIntersectionCorrDF(corrDF,differenceStock)

def getAverageCorr(intersectionCorrDF,stockList,classification):
    classificationDF=pd.DataFrame(classification,index=stockList,columns=['classification'])
    newCorrDF=pd.concat([classificationDF,corrDF],axis=1)
    category=sorted(list(set(classification)))
    number=[0]*len(category)
    for n in range(len(category)):
        number[n]=classification.count(category[n])
    internalAverageCoef=[0]*len(category)
    externalAverageCoef=[0]*len(category)
    for i in range(len(category)):
        tmpDF=newCorrDF[newCorrDF['classification'].isin([category[i]])]
        internalDF=tmpDF.loc[:,[stock for stock in tmpDF.index]]
        externalDF=tmpDF.loc[:,[stock for stock in tmpDF.columns if stock not in tmpDF.index]]
        s1=internalDF.sum(axis=1)
        ss1=0
        for j in range(len(s1)):
            ss1=ss1+s1[j]
            
        s2=externalDF.sum(axis=1)
        ss2=0
        for j in range(len(s2)):
            ss2=ss2+s2[j]
            
        internalAverageCoef[i]=(ss1-len(s1))/((len(s1)-1)*(len(s1)-1))
        externalAverageCoef[i]=ss2/(len(s2)*len(externalDF.T))
        
    f=open(r'd:\classification\averageCorr\SW.txt','w')
    for k in range(len(internalAverageCoef)):
        f.write('%s\t%d\t%f\t%f\t%f\t%f\n'%(category[k],number[k],internalAverageCoef[k],externalAverageCoef[k],internalAverageCoef[k]-externalAverageCoef[k],std[k]))
        
    f.write('avg\t%f\t%f\t%f\t%f\t%f\n'%(float(sum(number))/len(number),sum(internalAverageCoef)/len(internalAverageCoef),sum(externalAverageCoef)/len(externalAverageCoef),sum(internalAverageCoef)/len(internalAverageCoef)-sum(externalAverageCoef)/len(externalAverageCoef),sum(std)/len(std)))
    f.close()
    return (internalAverageCoef,externalAverageCoef)
    
(internalAverageCoef,externalAverageCoef)=getAverageCorr(intersectionCorrDF,stockList,classification)

def getCrossCorrDF(intersectionCorrDF,stockList,classification):
    classificationDF=pd.DataFrame(classification,index=stockList,columns=['classification'])
    newCorrDF=pd.concat([classificationDF,corrDF],axis=1)
    category=sorted(list(set(classification)))
    crossCorrDF=pd.DataFrame(np.random.randn(len(category),len(category)),index=category,columns=category)
    for i in range(len(category)):
        tmpDF=newCorrDF[newCorrDF['classification'].isin([category[i]])]
        for j in range(i+1,len(category)):
            
            crossStock=newCorrDF[newCorrDF['classification'].isin([category[j]])].index
            crossDF=tmpDF.loc[:,[stock for stock in crossStock]]
            crossS=crossDF.sum(axis=1)
            crossSS=0
            for k in range(len(crossS)):
                crossSS=crossSS+crossS[k]
            crossCorr=crossSS/(len(tmpDF)*len(crossStock))
#            print category[i],category[j],crossCorr
            crossCorrDF.iat[i,j]=crossCorr
            crossCorrDF.iat[j,i]=crossCorr
        crossCorrDF.iat[i,i]=1
    
    return crossCorrDF
        
crossCorrDF=getCrossCorrDF(intersectionCorrDF,stockList,classification)
crossCorrDF.to_csv(r'd:\classification\averageCorr\SW.csv')



end=time.time()
print end-start

