# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 13:42:44 2016

@author: zht
"""

import os
import numpy as np
import time
import sys
import pandas as pd
import pylab as pl

start=time.time()
reload(sys)
sys.setdefaultencoding('utf-8')

def function(length,withdraw):
    def getAllFilePath(path):  #三层目录c
        fileNameList=[]
        filePathList=[]
        firstClassFolderName=os.listdir(path)
        for i in firstClassFolderName:
            firstClassPathName=os.path.join('%s\%s'%(path,i))
            secondClassFolderName=os.listdir(firstClassPathName)
            for j in  secondClassFolderName:
                secondClassPathName=os.path.join('%s\%s'%(firstClassPathName,j))
                for fileName in os.listdir(secondClassPathName):
                    filePath=os.path.join('%s\%s'%(secondClassPathName,fileName))
                    fileNameList.append(fileName)
                    filePathList.append(filePath)
        return (filePathList,fileNameList)
    
    (filePathList,fileNameList)=getAllFilePath('d:\\bloomberg')#注意一般情况下此处要将日期排序，由于此处读进来已经排好序，不必排了,可以用timeS=time.strptime(s,'%Y%m%d')转时间格式
    #判断排序是否正确
    #for i in range(1,len(fileNameList)):
    #    if int(fileNameList[i][-8:])-int(fileNameList[i-1][-8:])<=0:
    #        print i,fileNameList[i],fileNameList[i-1]
    def getDateList(fileNameList):
        dateList=['']*len(fileNameList)
        for i in range(len(fileNameList)):
            dateList[i]=fileNameList[i][-8:]
        return dateList
    
    dateList=getDateList(fileNameList)
    
    def getNameListAndPriceList(filePath):#收盘价
        line=open(filePath).read().split('\n')
        nameList=['']*(len(line))
        priceList=['']*(len(line))
        #某些数据后边有两个\n,有些数据最后边只有一个\n
        tmp=len(line)-1
        while True:
            if line[tmp]=='':
                del line[tmp]
                tmp-=1
            else:
                break
        for i in range(len(line)):
            nameList[i]=line[i].split(',')[3]
            priceList[i]=float(line[i].split(',')[5])
        #return (name,price)
        #某些name和price的最后一个数据为空或99999，此处将其处理
        tmp2=len(line)-1
        while True:
            if nameList[tmp2]=='99999' or nameList[tmp2]=='':
                del nameList[tmp2]
                del priceList[tmp2]
                tmp2-=1
            else:
                break
        #待解决问题，最后一个元素为''好像还是没解决（99999已经去除）
        while '' in nameList:
            nameList.remove('')
        while '' in priceList:
            priceList.remove('')
            
        index=[]
        for i in range(len(nameList)):
            if nameList[i][0]=='1' or nameList[i][0]=='2' or nameList[i][0]=='9':
                index.append(i)
        for i in index[::-1]:
            del nameList[i]
            del priceList[i]  
        return (nameList,priceList)
    
    def getDataFrameForSomeDay(nameList,priceList,fileName):
        col=[fileName[-8:]]
        df=pd.DataFrame(priceList,index=nameList,columns=col)
        return df
    
    def getDfList(fileNameList,filePathList):
        dfList=['']*len(filePathList)
        for i in range(len(filePathList)):
            (nameList,priceList)=getNameListAndPriceList(filePathList[i])
            fileName=fileNameList[i]
            dfList[i]=getDataFrameForSomeDay(nameList,priceList,fileName)
        return dfList
    
    def getMergedDataFrame(fileNameList,filePathList):
        dfList=['']*len(filePathList)
        for i in range(len(filePathList)):
            (nameList,priceList)=getNameListAndPriceList(filePathList[i])
            fileName=fileNameList[i]
            dfList[i]=getDataFrameForSomeDay(nameList,priceList,fileName)
        mergedDataFrame=dfList[0]
        for i in range(1,len(dfList)):
            mergedDataFrame=pd.concat([mergedDataFrame,dfList[i]],axis=1)
        return mergedDataFrame
    
    mergedDataFrame=getMergedDataFrame(fileNameList,filePathList)
    
    dataFrame=mergedDataFrame.T
    
    def getReturnDataFrame(dataFrame):
        rList=['']*len(dataFrame.T)
        index=dataFrame.T.index
        for i in range(len(rList)):
    #        rList[i]=(dataFrame['%s'%(dataFrame.T.index[i])]-dataFrame['%s'%(dataFrame.T.index[i])].shift(1))/dataFrame['%s'%(dataFrame.T.index[i])].shift(1))
            rList[i]=(dataFrame[index[i]]-dataFrame[index[i]].shift(1))/dataFrame[index[i]].shift(1)
        returnDataFrame=rList[0]
        for i in range(1,len(rList)):
            returnDataFrame=pd.concat([returnDataFrame,rList[i]],axis=1)
        return returnDataFrame
        
    returnDataFrame=getReturnDataFrame(dataFrame)
    
    def getNameTableAndPriceTable(filePathList):
        nameTable=['']*len(dateList)
        priceTable=['']*len(dateList)
        for i in range(len(dateList)):
            (nameTable[i],priceTable[i])=getNameListAndPriceList(filePathList[i])
        return (nameTable,priceTable)
        
    (nameTable,priceTable)=getNameTableAndPriceTable(filePathList)#nameTable[i][j],i is the index of someday,j is the index of stock
    
    def getNewStock(name1,name2):
        return list(set(name2).difference(set(name1)))
    def getOldStock(name1,name2):
        return list(set(name2).union(set(name1)))
        
    
    def getIpoStockTable(nameTable):
        newStockTable=['']*len(fileNameList)
        oldStockTable=['']*len(fileNameList)
        ipoStockTable=['']*len(fileNameList)
        oldStockTable[0]=nameTable[0]
        ipoStockTable[0]=[]
        #mark=0
        for i in range(1,len(fileNameList)):
            newStockTable[i]=getNewStock(nameTable[i-1],nameTable[i])
    #        oldStockTable[i]=list(nameTable[i-1])
    #        oldStockTable[i].extend(newStockTable[i])
            oldStockTable[i]=getOldStock(oldStockTable[i-1],nameTable[i])
            ipoStockTable[i]=list(set(newStockTable[i]).difference(set(oldStockTable[i-1])))
        return (newStockTable,oldStockTable,ipoStockTable)#[i][j],i表示某一天，j表示当天上市的某只股票
        #return ipoStockTable
    (newStockTable,oldStockTable,ipoStockTable)=getIpoStockTable(nameTable)
    
    def getIpoStockList(ipoStockTable):
        ipoStockList=[]
        for i in range(1,len(ipoStockTable)):
            if ipoStockTable[i]!=[]:
                ipoStockList.extend(ipoStockTable[i])
        return ipoStockList
    
    ipoStockList=getIpoStockList(ipoStockTable)
    
    def getIpoStockReturnDataFrameAndIpoStockPriceDataFrame(ipoStockList,returnDataFrame,dataFrame):
        ipoStockReturnDataFrame=returnDataFrame[[i for i in ipoStockList]]
        ipoStockPriceDataFrame=dataFrame[[i for i in ipoStockList]]
        return (ipoStockReturnDataFrame,ipoStockPriceDataFrame)
        
    (ipoStockReturnDataFrame,ipoStockPriceDataFrame)=getIpoStockReturnDataFrameAndIpoStockPriceDataFrame(ipoStockList,returnDataFrame,dataFrame)
    
    
    def delBizarraStock(ipoStockReturnDataFrame,ipoStockPriceDataFrame):
        tmp1=ipoStockReturnDataFrame[ipoStockReturnDataFrame>=0.11]
        tmp2=ipoStockReturnDataFrame[ipoStockReturnDataFrame<=-0.11]
        tmp1=tmp1.fillna(0)
        tmp2=tmp2.fillna(0)
        for j in range(len(ipoStockReturnDataFrame.T)):
            for i in range(len(ipoStockReturnDataFrame)):
                if tmp1.iat[i,j]!=0:
                    ipoStockReturnDataFrame.iloc[:,j]=0#把奇异股票的收益率变为0
                    ipoStockPriceDataFrame.iloc[:,j]=0.0001#把奇异股票的股价全部变为1
                    break
        for j in range(len(ipoStockReturnDataFrame.T)):
            for i in range(len(ipoStockReturnDataFrame)):
                if tmp2.iat[i,j]!=0:
                    ipoStockReturnDataFrame.iloc[:,j]=0
                    ipoStockPriceDataFrame.iloc[:,j]=0.0001
                    break
        validReturnDataFrame=ipoStockReturnDataFrame
        validPriceDataFrame=ipoStockPriceDataFrame
        return (validReturnDataFrame,validPriceDataFrame)
        
    (validReturnDataFrame,validPriceDataFrame)=delBizarraStock(ipoStockReturnDataFrame,ipoStockPriceDataFrame)
    
    def adjustIpoStockReturnDataFrameAndIpoStockPriceDataFrame(validReturnDataFrame,validPriceDataFrame):
        adjustedReturnDataFrame=validReturnDataFrame.fillna(0)
        adjustedIpoStockPriceDataFrame=validPriceDataFrame.fillna(0)
        return (adjustedReturnDataFrame,adjustedIpoStockPriceDataFrame)
        
    (adjustedReturnDataFrame,adjustedIpoStockPriceDataFrame)=adjustIpoStockReturnDataFrameAndIpoStockPriceDataFrame(validReturnDataFrame,validPriceDataFrame)
    
    def getHoldDayList(adjustedIpoStockPriceDataFrame,ipoStockList,withdraw):
        holdDayList=['']*len(ipoStockList)
        for j in range(len(ipoStockList)):
            listedDay=0
            for i in range(len(adjustedIpoStockPriceDataFrame)):
                if adjustedIpoStockPriceDataFrame.iat[i,j]==0:
                    listedDay+=1
                else:
                    break
            maxDay=listedDay
            maxPrice=adjustedIpoStockPriceDataFrame.iat[maxDay,j]
            for k in range(listedDay+1,len(adjustedIpoStockPriceDataFrame)):
                if adjustedIpoStockPriceDataFrame.iat[k,j]>=adjustedIpoStockPriceDataFrame.iat[k-1,j]:
                    maxDay+=1
                    maxPrice=adjustedIpoStockPriceDataFrame.iat[maxDay,j]
                else:
                    break
                
            buyingDay=maxDay
            for m in range(maxDay+1,len(adjustedIpoStockPriceDataFrame)):
                if (maxPrice-adjustedIpoStockPriceDataFrame.iat[m,j])/adjustedIpoStockPriceDataFrame.iat[m,j]>=withdraw:
                    buyingDay=m
                    break
                else:
                    buyingDay=len(adjustedIpoStockPriceDataFrame)-1
            
            holdDayList[j]=buyingDay
        return holdDayList
                    
    holdDayList=getHoldDayList(adjustedIpoStockPriceDataFrame,ipoStockList,withdraw)  
    
    def getHoldReturnDF(holdDayList,adjustedReturnDataFrame,ipoStockList,dateList,length):
        l=length
        holdReturnDF=pd.DataFrame(np.random.randn(len(dateList),len(ipoStockList)),index=dateList,columns=ipoStockList)#获得dataframe
        holdReturnDF.iloc[:,:]=0#所有元素初始化为0
        for j in range(len(ipoStockList)):
            endDay=0
            if holdDayList[j]+l>=len(dateList)-1:
                endDay=len(dateList)-1
            else:
                endDay=holdDayList[j]+l
            for i in range(holdDayList[j],endDay):
                holdReturnDF.iat[i,j]=adjustedReturnDataFrame.iat[i,j]
        holdReturnDF.fillna(0)
        return holdReturnDF
    holdReturnDF=getHoldReturnDF(holdDayList,adjustedReturnDataFrame,ipoStockList,dateList,length)
    
    def getInitialValue(holdReturnDF):
        countList=['']*len(holdReturnDF)
        for i in range(len(holdReturnDF)):
            countList[i]=0
            for j in range(len(ipoStockList)):
                if holdReturnDF.iat[i,j]!=0:
                    countList[i]+=1
        initialValue=max(countList)
        return initialValue
    initialValue=getInitialValue(holdReturnDF)
    
    def getValueVariationDF(holdDayList,adjustedIpoStockPriceDataFrame,ipoStockList,length):
        l=length
        valueVariationDF=pd.DataFrame(np.random.randn(len(dateList),len(ipoStockList)),index=dateList,columns=ipoStockList)#获得dataframe
        valueVariationDF.iloc[:,:]=0#所有元素初始化为0
        for j in range(len(ipoStockList)):
            bidPrice=adjustedIpoStockPriceDataFrame.iat[holdDayList[j],j]
            endDay=holdDayList[j]
            if holdDayList[j]+l>len(dateList)-1:
                endDay=len(dateList)-1
            else:
                endDay=holdDayList[j]+l
            if adjustedIpoStockPriceDataFrame.iat[endDay,j]==0:
                endDay+=1
            if endDay>=len(dateList)-1:
                endDay=len(dateList)-1
            
            valueVariationDF.iat[endDay,j]=(adjustedIpoStockPriceDataFrame.iat[endDay,j]-bidPrice)/bidPrice
        return valueVariationDF
    valueVariationDF=getValueVariationDF(holdDayList,adjustedIpoStockPriceDataFrame,ipoStockList,length)
    
    def getValueVariationSeries(valueVariationDF):
        variationSeries=list(valueVariationDF.sum(axis=1))
        return variationSeries
    valueVariationSeries=getValueVariationSeries(valueVariationDF)
    
    def getAccumulativeReturnSeries(valueVariationSeries,initialValue):
        accumulativeReturnSeries=['']*len(valueVariationSeries)
        accumulativeReturnSeries[0]=0
        s=initialValue
        for i in range(1,len(valueVariationSeries)):
            s=s+valueVariationSeries[i]
            accumulativeReturnSeries[i]=(s-initialValue)/initialValue
        return accumulativeReturnSeries
    
    accumulativeReturnSeries=getAccumulativeReturnSeries(valueVariationSeries,initialValue)
    
    y=accumulativeReturnSeries
    x=dateList
    pl.plot(x,y)
    pl.title('length=%d  withdraw=%.2f'%(length,withdraw))
    pl.xlabel('date')
    pl.ylabel('return')
    pl.savefig('d:\harden\%.2f_%.2f.png'%(length,withdraw))
    pl.show()

#for zhanghaitao in range(10,27,2):
#    for cxt in np.arange(0.05,0.17,0.02):
#        function(zhanghaitao,cxt)

function(10,0.08)

 