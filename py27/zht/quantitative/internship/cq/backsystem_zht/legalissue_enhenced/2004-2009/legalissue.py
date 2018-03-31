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


dd=open(r'data2010-2016.txt').read().split('\n')[:-1]
name_raw=dd[0].split('\t')
name=dd[1].split('\t')
datatype=dd[2].split('\t')
data=[r.split('\t') for r in dd[3:]]
#just test data after 2010
data=[d for d in data if 20160812>int(d[1])>=20100104]
title=zip(name_raw,name,datatype,range(len(name_raw)))
variables=[Variable(t[0],t[1],t[2],t[3]) for t in title if t[2] in ['c','d']]

def get_grade_dict(fill_value=0):
    variables_d=[v for v in variables if v.datatype=='d']
    grade_dict={}
    for variable_d in variables_d:
        file_names=os.listdir('observe_variable')
        #cuz some variable may have too little samples resulting in 
        #no fig and variable_descriptiion file produced in observe_variable folder
        if '%s_description.txt'%variable_d.name in file_names:
            lines=open(r'observe_variable\%s_description.txt'%variable_d.name).read().split('\n')[:-1]
            tmp_dict={}
            for l in lines:
                key=l.split('\t')[1]
                tmp_dict.setdefault(key,0)
                #some value may be invalid,so using try to make it compatible
                try:
                    value=float(l.split('\t')[2])
                    if abs(value)<0.07:
                        tmp_dict[key]=0.07**2
                    elif value>0.05:
                        tmp_dict[key]=fill_value
                    elif value<0:
                        tmp_dict[key]=abs(value)**2
                except:
                    pass
            grade_dict[variable_d.name]=tmp_dict
    return grade_dict

def get_alpha(grade_dict,nan_value=0.01):
    alpha=[]
    for d in data:
        grades=[]
        for grade_d in grade_dict:
            col_index=[int(t[3]) for t in title if t[1]==grade_d][0]
            v=d[col_index]
            if v in grade_dict[grade_d]:
                grade=grade_dict[grade_d][v]
            else:
                #some value is not in dict,so give them a nonzero value,this 
                #value can be adjust to better fit the model
                grade=nan_value
                
            grades.append(grade)
        
        final_grade=np.cumprod(grades)[-1]
        
        stock=d[0]
        date=d[1]
        start_date=shift_date(date)
        end_date=start_date
        alpha.append((stock,start_date,end_date,(-1.0)*final_grade))
        print date
    return alpha

grade_dict=get_grade_dict()
alpha=get_alpha(grade_dict)

position=alpha_to_position(alpha)
pnl=position_to_pnl(position)
plot1(pnl,r'quadratic\test.png')
print fill_value,nan_value
position_to_alpha_file1(position)










