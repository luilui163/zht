# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 13:42:44 2016

@author: Administrator
"""

import os
import numpy as np
import time
import sys
import pandas as pd
start=time.time()

reload(sys)
sys.setdefaultencoding('utf-8')

def  getAllFilePath(path):  #三层目录c
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


def getNameListAndPriceList(filePath):
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
        priceList[i]=line[i].split(',')[5]
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
    return (nameList,priceList)
    
    

(filePathList,fileNameList)=getAllFilePath('d:\\bloomberg')


def getNameTableAndPriceTable(filePathList):
    nameTable=[[0 for j in range(5000)] for i in range(len(fileNameList))]
    priceTable=[[0 for j in range(5000)] for i in range(len(fileNameList))]
    for i in range(len(filePathList)):
        (nameTable[i],priceTable[i])=getNameListAndPriceList(filePathList[i])
    return( nameTable,priceTable)

(nameTable,priceTable)=getNameTableAndPriceTable(filePathList)#nameTable[i][j],i is the index of someday,j is the index of stock

def getNewStock(name1,name2):
    return list(set(name2).difference(set(name1)))
def getOldStock(name1,name2):
    return list(set(name2).union(set(name1)))
    
def getIpoStockTable(nameTable):
    newStockTable=[[0 for j in range(5000)]for i in range(len(nameTable))]
    oldStockTable=[[0 for j in range(5000)]for i in range(len(nameTable))]
    ipoStockTable=[[0 for j in range(5000)]for i in range(len(nameTable))]
    oldStockTable[0]=nameTable[0]
    #mark=0
    for i in range(1,len(nameTable)):
        newStockTable[i]=getNewStock(nameTable[i-1],nameTable[i])
#        oldStockTable[i]=list(nameTable[i-1])
#        oldStockTable[i].extend(newStockTable[i])
        oldStockTable[i]=getOldStock(oldStockTable[i-1],nameTable[i])
        ipoStockTable[i]=list(set(newStockTable[i]).difference(set(oldStockTable[i-1])))
    return (newStockTable,oldStockTable,ipoStockTable)#[i][j],i表示某一天，j表示当天上市的某只股票
    #return ipoStockTable
(newStockTable,oldStockTable,ipoStockTable)=getIpoStockTable(nameTable)
#注意，此处没有排除数据中非股票数据，还需要限定为0,3,6开头的数据

def getIpoStockList(ipoStockTable):
    ipoStockList=[]
    for i in range(1,len(ipoStockTable)):
        if ipoStockTable[i]!=[]:
            ipoStockList.extend(ipoStockTable[i])
    return ipoStockList

ipoStockList=getIpoStockList(ipoStockTable)





stockList=oldStockTable[-1]
while '' in stockList:
    stockList.remove('')

def generateTxtForStock(stockList):
    for i in range(len(stockList)):
        f=open('d:\\timeSeries\%s.txt'%stockList[i],'w')
        f.close()

generateTxtForStock(stockList)

def getTimeList(fileNameList):
    timeList=['']*len(fileNameList)
    for i in range(len(fileNameList)):
        timeList[i]=fileNameList[i][-8:]
    return timeList
    
timeList=getTimeList(fileNameList)

def writeData(stockList,nameTable,priceTable,timeList):
    dateSeriesTable=['']*len(stockList)
    priceSeriesTable=['']*len(stockList)
    for k in range(len(stockList)):
        f=open('d:\\timeSeries\%s.txt'%stockList[k],'w')
        dateSeriesTable[k]=['']*len(nameTable)
        priceSeriesTable[k]=['']*len(nameTable)
        for i in range(len(nameTable)):
            if stockList[k] in nameTable[i]:
                if priceTable[i][nameTable[i].index(stockList[k])]!='99999'and priceTable[i][nameTable[i].index(stockList[k])]!='99999.00':
                    f.write('%s\t%.2f\n'%(timeList[i],float(priceTable[i][nameTable[i].index(stockList[k])])))
                    dateSeriesTable[k][i]=timeList[i]
                    priceSeriesTable[k][i]=float(priceTable[i][nameTable[i].index(stockList[k])])
            else:
                pass
        f.close()
    for i in range(len(dateSeriesTable)):
        while '' in dateSeriesTable[i]:
            dateSeriesTable[i].remove('')
            priceSeriesTable[i].remove('')
    return (dateSeriesTable,priceSeriesTable)
    #dateSeriesTable[k][i],k表示某只股票，i表示某个交易日      
(dateSeriesTable,priceSeriesTable)=writeData(stockList,nameTable,priceTable,timeList)
'''
def writeData(stockList,nameTable,priceTable,timeList):
    dateSeriesTable=[[-1 for j in range(len(timeList))]for i in range(len(stockList))]
    priceSeriesTable=[[-1 for j in range(len(timeList))]for i in range(len(stockList))]
    for k in range(len(stockList)):
        f=open('d:\\timeSeries\%s.txt'%stockList[k],'w')
        for i in range(len(nameTable)):
            if stockList[k] in nameTable[i]:
                if priceTable[i][nameTable[i].index(stockList[k])]!='99999'and priceTable[i][nameTable[i].index(stockList[k])]!='99999.00':
                    f.write('%s\t%.2f\n'%(timeList[i],float(priceTable[i][nameTable[i].index(stockList[k])])))
                    dateSeriesTable[k][i]=timeList[i]
                    priceSeriesTable[k][i]=float(priceTable[i][nameTable[i].index(stockList[k])])
            else:
                pass
        f.close()
    for i in range(len(dateSeriesTable)):
        while '' in dateSeriesTable[i]:
            dateSeriesTable[i].remove('')
            priceSeriesTable[i].remove('')
    return (dateSeriesTable,priceSeriesTable)
    #dateSeriesTable[k][i],k表示某只股票，i表示某个交易日      
(dateSeriesTable,priceSeriesTable)=writeData(stockList,nameTable,priceTable,timeList)
'''



#def getMa5(dateSeriesTable,priceSeriesTable):
#    ma5DateTable=['']*len(dateSeriesTable)
#    ma5PriceTable=['']*len(dateSeriesTable)
#    for i in range(len(dateSeriesTable)):
#        ma5DateTable[i]=dateSeriesTable[i][4:]
#        tmpList=['']*len((priceSeriesTable[i]))
#        for j in range(4,len(priceSeriesTable[i])):
#            tmpList[j]=(priceSeriesTable[i][j-4]+priceSeriesTable[i][j-3]+priceSeriesTable[i][j-2]+priceSeriesTable[i][j-1]+priceSeriesTable[i][j])/5.0
#        while '' in tmpList:
#            tmpList.remove('')
#        ma5PriceTable[i]=tmpList
#    return (ma5DateTable,ma5PriceTable)
#
#(ma5DateTable,ma5PriceTable)=getMa5(dateSeriesTable,priceSeriesTable)
#
#def getSignTable(priceSeriesTable,ma5PriceTable):
#    signTable=['']*len(priceSeriesTable)
#    for i in range(len(priceSeriesTable)):
#        tmp=priceSeriesTable[i][4:]
#        signTable[i]=map(lambda (a,b):a-b,zip(tmp,ma5PriceTable[i]))
#        for j in range(len(signTable[i])):
#            if signTable[i][j]<0:
#                signTable[i][j]=-1
#            elif signTable[i][j]>0:
#                signTable[i][j]=1
#    return signTable
#    
#signTable=getSignTable(priceSeriesTable,ma5PriceTable)
##第一个数据是开盘后的第四天的数据，因为之前的数据没有5日的移动平均价
'''
def getReturnTable(timeList,stockList,priceSeriesTable):
    #returnTable=[[0 for j in range(len(priceSeriesTable))] for i in range(5000)]
    returnTable=[[0 for j in range(len(timeList))] for i in range(len(stockList))]
    for i in range(len(stockList)):
        tmp=['']*(len(timeList)+1)
        tmp[0]=1
        tmp[1:]=priceSeriesTable[i]
        returnTable[i]=map(lambda (a,b):(b-a)/a,zip(tmp,priceSeriesTable[i]))
        #注意returnTable[i][0]的数据是无效数据，
    return returnTable
'''
def getReturnTable(timeList,stockList,nameTable,dateSeriesTable,priceSeriesTable):
    #returnTable=[[0 for j in range(len(priceSeriesTable))] for i in range(5000)]
    tmp=[[0 for j in range(len(timeList))] for i in range(len(stockList))]
    for i in range(len(stockList)):
        m=['']*(len(timeList)+1)
        m[0]=1
        m[1:]=priceSeriesTable[i]
        tmp[i]=map(lambda (a,b):(b-a)/a,zip(m,priceSeriesTable[i]))
        #注意returnTable[i][0]的数据是无效数据，
        

    returnTable=[[0 for j in range(len(timeList))] for i in range(len(stockList))] 
    for i in range(len(tmp)):
        for j in range(len(tmp[i])):
            returnTable[i][timeList.index(dateSeriesTable[i][j])]=tmp[i][j]
    return returnTable
    
        

    
returnTable=getReturnTable(timeList,stockList,nameTable,dateSeriesTable,priceSeriesTable)

#for i in range(len(returnTable[0])):
#    print i,'\t',priceSeriesTable[0][i],'\t',returnTable[0][i]

def getHoldDayList(priceSeriesTable):
    holdDayList=['']*len(priceSeriesTable)
    for i in range(len(priceSeriesTable)):
        holdDayList[i]=-1
        maxIndex=0
        for m in range(len(priceSeriesTable[i])):
            if priceSeriesTable[i][m]!=0:
                max=priceSeriesTable[i][m]#第一个不是0的元素
                maxIndex=m
                break
        for j in range(m+1,len(priceSeriesTable[i])):
            if priceSeriesTable[i][j]>=priceSeriesTable[i][j-1]:#此处不考虑期间可能停牌，
                max=priceSeriesTable[i][j]
                maxIndex=j
            else:
                break
        for k in range(maxIndex+1,len(priceSeriesTable[i])):
            if (max-priceSeriesTable[i][k])/max>=0.2:
                holdDayList[i]=k
                break
    return holdDayList

holdDayList=getHoldDayList(priceSeriesTable)    

#for i in range(len(holdDayList)):
#    if holdDayList[i]!=0:
#        print i,holdDayList[i]

#def getExchangeTable(stockList,fileNameList,dateSeriesTable):
#    exchangeTable=[[0 for j in range(len(timeList))] for i in range(len(stockList))]
#    for i in range(len(stockList)):
#        for j in range(len(dateSeriesTable[i])):
#            exchangeTable[i][timeList.index(dateSeriesTable[i][j])]=returnTable[i][j]
#    return exchangeTable
#    
#exchangeTable=getExchangeTable(stockList,fileNameList,dateSeriesTable)


#def getStartDateAndEndDate(holdDayList):
#    startDate=['']*len(stockList)
#    endDate=['']*len(stockList)
#    for i in range(len(stockList)):
#        index=0
#        for j in range(len(stockList[i])):
#            if stockList[i][j]!=0:
#                index=j
#                break
#        count=0 
#        m=0
#        for k in range(index,len(stockList[i])):
#            m+=1
#            if stockList[i][k]!=0:
#                count+=1
#            if count==10:
#                break
#        startDate[i]=timeList[index+holdDayList[i]]
#        if index+holdDayList[i]+m<=len(timeList)-1:
#            endDate[i]=timeList[index+holdDayList[i]+m]
#        else:
#            endDate[i]=startDate[i]
#    return (startDate,endDate)
'''
def getStartNumberAndendNumber(holdDayList):
    startNumber=['']*len(stockList)
    endNumber=['']*len(stockList)
    for i in range(len(stockList)):
        index=0
        for j in range(len(stockList[i])):
            if stockList[i][j]!=0:
                index=j
                break
        count=0
        m=0
        for k in range(index,len(stockList[i])):
            m+=1
            if stockList[i][k]!=0:
                count+=1
            if count==10:
                break
        startNumber[i]=index+holdDayList[i]
        if index+holdDayList[i]+m<=len(timeList)-1:#排除那些无法交易的数据
            endNumber[i]=index+holdDayList[i]+m
        else:
            endNumber[i]=startNumber[i]
    return (startNumber,endNumber)
'''
#def getStartNumberAndendNumber(holdDayList):
#    startNumber=holdDayList
#    endNumber=['']*len(stockList)
#    for i in range(len(stockList)):
#        count=0
#        for j in range(holdDayList[i],len(timeList)):
#            if j>=len(priceSeriesTable[i]):
#                break
#            if priceSeriesTable[i][j]!=0:
#                count+=1
#            if count==10:
#                endNumber[i]=j
#                break
#    return (startNumber,endNumber)
#    
#(startNumber,endNumber)=getStartNumberAndendNumber(holdDayList)


#for i in range(len(stockList)):
#        print len(timeList),i,startNumber[i],endNumber[i],endNumber[i]-startNumber[i]


'''
adjustedReturnTable=[[0 for j in range(len(timeList))]for i in range(len(stockList))]
indexList=['']*len(ipoStockList)
for k in range(len(ipoStockList)):
    indexList[k]=stockList.index(ipoStockList[k])
indexList.sort()
for i in range(len(stockList)):
    print i,startNumber[i],endNumber[i]


'''
#for i in indexList:
#    for j in range(startNumber[i],endNumber[i]+1):
#        print i,j,returnTable[i]

def getAdjustedReturnTable(returnTable,ipoStockList,holdDayList):
    adjustedReturnTable=[[0 for j in range(len(timeList))]for i in range(len(stockList))]
    indexList=['']*len(ipoStockList)
    for k in range(len(ipoStockList)):
        indexList[k]=stockList.index(ipoStockList[k])
    indexList.sort()
    for i in indexList:
        for j in range(holdDayList[i],holdDayList[i]+10):
            if holdDayList[i]+10>=len(returnTable[i]):
                pass
            adjustedReturnTable[i][j]=returnTable[i][j]
    return adjustedReturnTable
    
adjustedReturnTable=getAdjustedReturnTable(returnTable,ipoStockList,holdDayList)

def getTotalReturnSeries(adjustedReturnTable,timeList):
    totalReturnSeries=['']*len(timeList)
    for i in range(len(totalReturnSeries)):
        totalReturnSeries[i]=0
        count=0
        for j in range(len(adjustedReturnTable)):
            if adjustedReturnTable[j][i]!=0:
                count+=1
                totalReturnSeries[i]+=adjustedReturnTable[j][i]
        if totalReturnSeries[i]!=0:
            totalReturnSeries[i]=totalReturnSeries[i]/count
        if totalReturnSeries[i]>0.11 or totalReturnSeries<-0.11:
            del totalReturnSeries[i]
    return totalReturnSeries

totalReturnSeries=getTotalReturnSeries(adjustedReturnTable,timeList)

f=open('d:\\harden\return.txt','w')
for i in range(len(totalReturnSeries)):
    f.write(totalReturnSeries[i])

        




end=time.time()
timelenght=end-start
print timelenght


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    