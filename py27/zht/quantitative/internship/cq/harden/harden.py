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
        firstClassPathName=os.path.join('%s/%s'%(path,i))
        secondClassFolderName=os.listdir(firstClassPathName)
        for j in  secondClassFolderName:
            secondClassPathName=os.path.join('%s/%s'%(firstClassPathName,j))
            for fileName in os.listdir(secondClassPathName):
                filePath=os.path.join('%s/%s'%(secondClassPathName,fileName))
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
        priceList[i]=line[i].split(',')[4]
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
    
    

(filePathList,fileNameList)=getAllFilePath('/home/hzhang/bloomberg')


'''
def findNewStock(name1,name2):
    return list(set(name2).difference(set(name1)))
'''   
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
        oldStockTable[i]=list(nameTable[i-1])
        oldStockTable[i].extend(newStockTable[i])
        ipoStockTable[i]=list(set(newStockTable[i]).difference(set(oldStockTable[i-1])))
    return (newStockTable,oldStockTable,ipoStockTable)
    #return ipoStockTable
(newStockTable,oldStockTable,ipoStockTable)=getIpoStockTable(nameTable)
#注意，此处没有排除数据中非股票数据，还需要限定为0,3,6开头的数据

stockList=oldStockTable[-1]
while '' in stockList:
    stockList.remove('')

def generateTxtForStock(stockList):
    for i in range(len(stockList)):
        f=open('/home/hzhang/timeSeries/%s.txt'%stockList[i],'w')
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
        f=open('/home/hzhang/timeSeries/%s.txt'%stockList[k],'w')
        dateSeriesTable[k]=['']*len(nameTable)
        priceSeriesTable[k]=['']*len(nameTable)
        for i in range(len(nameTable)):
            if stockList[k] in nameTable[i]:
                if priceTable[i][nameTable[i].index(stockList[k])]!='99999':
                    f.write('%s/t%.2f\n'%(timeList[i],float(priceTable[i][nameTable[i].index(stockList[k])])))
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
    #dateSeriesTable[k][i],k表示某只股票，j表示某个交易日      
(dateSeriesTable,priceSeriesTable)=writeData(stockList,nameTable,priceTable,timeList)



def getMa5(dateSeriesTable,priceSeriesTable):
    ma5DateTable=['']*len(dateSeriesTable)
    ma5PriceTable=['']*len(dateSeriesTable)
    for i in range(len(dateSeriesTable)):
        ma5DateTable[i]=dateSeriesTable[i][4:]
        tmpList=['']*len((priceSeriesTable[i]))
        for j in range(4,len(priceSeriesTable[i])):
            tmpList[j]=(priceSeriesTable[i][j-4]+priceSeriesTable[i][j-3]+priceSeriesTable[i][j-2]+priceSeriesTable[i][j-1]+priceSeriesTable[i][j])/5.0
        while '' in tmpList:
            tmpList.remove('')
        ma5PriceTable[i]=tmpList
    return (ma5DateTable,ma5PriceTable)

(ma5DateTable,ma5PriceTable)=getMa5(dateSeriesTable,priceSeriesTable)

def getSignTable(priceSeriesTable,ma5PriceTable):
    signTable=['']*len(priceSeriesTable)
    for i in range(len(priceSeriesTable)):
        tmp=priceSeriesTable[i][4:]
        signTable[i]=map(lambda (a,b):a-b,zip(tmp,ma5PriceTable[i]))
        for j in range(len(signTable[i])):
            if signTable[i][j]<0:
                signTable[i][j]=-1
            elif signTable[i][j]>0:
                signTable[i][j]=1
    return signTable
    
signTable=getSignTable(priceSeriesTable,ma5PriceTable)
#第一个数据是开盘后的第四天的数据，因为之前的数据没有5日的移动平均价

def getReturnTable(priceSeriesTable):
    returnTable=[[0 for j in range(len(priceSeriesTable))] for i in range(5000)]
    for i in range(len(priceSeriesTable)):
        tmp=['']*5005
        tmp[0]=1
        tmp[1:]=priceSeriesTable[i]
        returnTable[i]=map(lambda (a,b):(b-a)/a,zip(tmp,priceSeriesTable[i]))
        #注意returnTable[i][0]的数据是无效数据，
    return returnTable

returnTable=getReturnTable(priceSeriesTable)
for i in range(len(returnTable[0])):
    print i,'\t',priceSeriesTable[0][i],'\t',returnTable[0][i]







end=time.time()
timelenght=end-start
print timelenght

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    