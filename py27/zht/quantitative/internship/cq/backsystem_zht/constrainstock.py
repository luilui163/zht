# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 12:19:19 2016

@author: hp
"""
import pandas as pd
import numpy as np
from util import *
import matplotlib.pyplot as plt
from process_data import Variable
import os
from itertools import combinations


'''
使用解禁日期，可以在解禁之前得知，有的解禁日期和公告日期相距很远，有的甚至解禁日期在公告日期之后。
在使用解禁日期之前先判断一下信息出来的时间（公告日期，信息抓取时间都得满足)是否在这之前。
'''


dd=open(r'data.txt').read().split('\n')[:-1]
name_raw=dd[0].split('\t')
name=dd[1].split('\t')
datatype=dd[2].split('\t')
data=[r.split('\t') for r in dd[3:]]
#just test data after 2010
data=[d for d in data if 20160812>int(d[1])>=20100104]
title=zip(name_raw,name,datatype,range(len(name_raw)))
variables=[Variable(t[0],t[1],t[2],t[3]) for t in title if t[2] in ['c','d']]






alphas={}

for k in range(100,len(data)):
    grades=[]
    
    #notice that using date to split the compare sample set will be more accurate
    compare_set=data[k-99:k+1]
    df=pd.DataFrame(compare_set,columns=[t[1] for t in title])
    rank_asc=df.rank()
    rank_des=df.rank(ascending=False)
    grades_asc=rank_asc.iloc[-1]
    grades_des=rank_des.iloc[-1]
    #max_grades=rank.max()
    
    '''
    how to deal with Nan value or invalid value
    '''
    #v3 the higher,the bigger the weight of short 
    variable_v3=[v for v in variables if v.name=='v3'][0]
    grade1=grades_asc[variable_v3.col]/100  #can consider about use max_grades=rank.max()
    grades.append(grade1)
    
    #v5 and v6 they are almost equal,the smaller the value,the bigger the weight of short
    variable_v5=[v for v in variables if v.name=='v5'][0]
    variable_v6=[v for v in variables if v.name=='v6'][0]
    g1=grades_des[variable_v5.col]/100
    g2=grades_des[variable_v6.col]/100
    grade2=(g1+g2)/2.0
    grades.append(grade2)
    
    #V7 and V8 are almost equal,if the value is abnomal enough,short it 
    variable_v7=[v for v in variables if v.name=='v7'][0]
    variable_v8=[v for v in variables if v.name=='v8'][0]
    g1=abs(grades_des[variable_v7.col]-rank_asc.iloc[:,variable_v7.col].median())/50
    g2=abs(grades_des[variable_v8.col]-rank_asc.iloc[:,variable_v8.col].median())/50
    grade3=(g1+g2)/2.0
    grades.append(grade3)    
    
    #v3,first get rank for the 8 values
    variable_v4=[v for v in variables if v.name=='v4'][0]
    items=open(r'observe_variable\%s_description.txt'%variable_v4.name).read().split('\n')[:-1]
    ranks={item.split('\t')[1]:(i+1)*1.0/len(items) for i,item in enumerate(items)}
    value_v4=df.iat[-1,variable_v4.col]
    if value_v4 in ranks:
        grade4=ranks[value_v4]
    else:
        grade4=0.5
    grades.append(grade4)

    #v9,when the value is 1 extremely strong ,2 is also strong
    variable_v9=[v for v in variables if v.name=='v9'][0]
    value_v9=df.iat[-1,variable_v9.col]
    if value_v9=='1':
        grade5=1
    else:
        grade5=0.1
    grades.append(grade5)
        
        
        
#===========================================================================
    stock=data[k][0]
    date=shift_date(data[k][1])
    combin=[]
    for n in range(1,len(grades)+1):
        combin+=list(combinations(''.join([str(i) for i in range(1,len(grades)+1)]),n))

    for cm in combin:
        if len(cm)>1:
            alphas.setdefault('_'.join(cm),[])
            alphas['_'.join(cm)].append((stock,date,date,(-1)*reduce(lambda x,y:x*y,[grades[int(c)-1] for c in cm])))
        else:
            alphas.setdefault('_'.join(cm),[])
            alphas['_'.join(cm)].append((stock,date,date,(-1)*grades[int(cm[0])-1]))
    print data[k][1]


for a in alphas:
    if not os.path.isdir(a):
        os.makedirs(a)
    position=alpha_to_position(alphas[a])
    pnl=position_to_pnl(position)
#    position_to_alpha_file1(position,a)
    if not os.path.isdir('fig'):
        os.makedirs('fig')
    figname='fig\%s.png'%a
    plot1(pnl,figname)
    print a

    
#'2_3_4_5' is best

#position=alpha_to_position(alphas['2_3_4_5'])
#position_to_alpha_file1(position,'2_3_4_5')









'''
def get_plain_position():
    weight=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    weight[weight==0]=np.nan
    alpha=[]
    for n,d in enumerate(data):
        try:
            stock=d[0]
            date=d[1]
            start_date=shift_date(date)
            end_date=shift_date(start_date,0)
            weight.loc[start_date:end_date,stock]=-1
            alpha.append((stock,start_date,end_date,-1))
        except:
            pass
        print n
    return weight,alpha

def get_weight1():
    variable=variables[4]
    weight1=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    weight1[weight1==0]=np.nan
    count=0
    for d in data:
        #some value may be invalid,we need to filter them 
        try:
            factor=float(d[variable.col])
            stock=d[0]
            date=d[1]
            start_date=shift_date(date)
            end_date=shift_date(start_date)
            
            if factor<25.0:
                weight1.loc[start_date:end_date,stock]=-1
                count+=1
        except:
            pass
        print count
    return weight1


#weight2 for v4
#first get rank for the 8 values
def get_weight2():
    variable=variables[3]
    weight2=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    weight2[weight2==0]=np.nan
    count=0
    for d in data:
        #some value may be invalid,we need to filter them 
        try:
            factor=float(d[variable.col])
            stock=d[0]
            date=d[1]
            start_date=shift_date(date)
            end_date=shift_date(start_date)
            
            if factor<65.0:
                weight2.loc[start_date:end_date,stock]=-1
                count+=1
            elif factor>=65:
                weight2.loc[start_date:end_date,stock]=1
                count+=1
        except:
            pass
        print count
    return weight2



#v5 and v6 they are almost equal,the smaller the value,the bigger the weight of short
def get_weight3():
    variable=variables[2]
    des=open(r'observe_variable\%s_description.txt'%variable.name).read().split('\n')[:-1]
    value_to_long=des[0].split('\t')[1]
    value_to_short=des[-1].split('\t')[1]
    
    weight3=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    weight3[weight3==0]=np.nan
    count=0
    for d in data:
        #some value may be invalid,we need to filter them 
        try:
            factor=d[variable.col]
            stock=d[0]
            date=d[1]
            start_date=shift_date(date)
            end_date=shift_date(start_date)
            
            if factor==value_to_long:
                weight3.loc[start_date:end_date,stock]=1
                count+=1
            elif factor==value_to_short:
                weight3.loc[start_date:end_date,stock]=-1
                count+=1
        except:
            pass
        print count
    return weight3

#V7 and V8 are almost equal,if the value is abnomal enough,short it 
def get_weight4():
    pass
'''

#weight1=get_weight1()
#weight2=get_weight2()
#weight3=get_weight3()
#position=reduce(pd.DataFrame.combineAdd,[weight1,weight2,weight3])
#
#pnl=position_to_pnl(position)
#figname='0jx.png'
#plot1(pnl,figname)
#
#position_to_alpha()



#contrast_position,alpha=get_plain_position()
#contrast_pnl=position_to_pnl(contrast_position)
#figname='contrast.png'
#plot1(contrast_pnl,figname)
#position_to_alpha_file(contrast_position)









