
#coding=utf-8
import math
#均值，方差，标准差，百分比，中位值之类的函数
def Average(List):
    average=0.00
    if len(List)<=0:
        pass
    else:
        average=round(float(sum(List))/float(len(List)),2)
    return average
 
def Variation(List):
    variation=0
    average=Average(List)
    if len(List)<=1:
        pass
    else:
        for i in range(len(List)):
            variation=variation+(List[i]-average)*(List[i]-average)
        variation = round(float(variation)/float(len(List)-1),2)
    return variation
def Std(List):
    variation = Variation(List)
    std = round(math.sqrt(variation),2)
    return std
def Proportion(List,index):
    prop = 0
    if index>1:
        pass
    else:
        List_Sort = sorted(List)
        Index = min(max((int(round(index*len(List)))-1),0),len(List))
        prop = List_Sort[Index]
    return prop
def Get_PropIndex(List,index):
    Index = 0
    if index>1:
        pass
    else:
        for i in range(len(List)):
            if Proportion(List,index) == List[i]:
                Index = i
                break
    return Index
def Get_MaxIndex(List):
    Index = 0
    for i in range(len(List)):
        if max(List) == List[i]:
            Index = i
            break
    return Index   
def Get_MinIndex(List):
    Index = 0
    for i in range(len(List)):
        if min(List) == List[i]:
            Index = i
            break
    return Index
def Percent_Sigma(List,Mean,Std):
    Percent = 0
    Low_Index = 0
    Up_Index = len(List)-1
    List_Sort = sorted(List)
   
    for i in range(0,len(List)):
        if List_Sort[i]>=(Mean-Std):
            Low_Index = i
            break
   
    for i in range(0,len(List)):
        if List_Sort[i]>=(Mean+Std):
            Up_Index = i
            break
       
   
    Percent = round((float(Up_Index - Low_Index + 1)/(len(List))),2)
    return Percent