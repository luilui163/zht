# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 16:28:51 2016

@author: hp
"""
import pandas as pd
import numpy as np
from util import *
import os

data=''
date=''

class Category:
    def __init__(self):
        pass
    
def statistic_continuous_variable(variable):
    variable.interval_number=5
#    lines=open('data.txt').read().split('\n')[:-1]
    
    raw_values=[]
    for d in data:
        #some values may be invalid,this will skip those values
        try:
            raw_values.append(float(d[variable.col]))
        except:
            pass
    raw_values.sort(reverse=True)
    variable.values=[]
    for i in range(variable.interval_number):
        variable.values.append(raw_values[int(len(raw_values)*i/variable.interval_number)])
    variable.values.append(raw_values[-1])
    
    if not os.path.isdir(r'%s\c'%str(date)):
        os.makedirs(r'%s\c'%str(date))
        
    with open(r'%s\c\%s.txt'%(date,variable.name),'w') as f:
        for value in variable.values:
            f.write('%f\n'%value)
    


def statistic_discrete_variable(variable):
    values={}
    for d in data:
        value=d[variable.col]
        values.setdefault(value,0)
        values[value]+=1
    variable.values=values
    
    if not os.path.isdir('d'):
        os.makedirs('d')
    
    counter=[]
    for value in variable.values:
        counter.append((value,variable.values[value]))
    counter.sort(key=lambda x:x[1],reverse=True)
    
    if not os.path.isdir(r'%s\d'%str(date)):
        os.makedirs(r'%s\d'%str(date))
    
    with open(r'%s\d\%s.txt'%(date,variable.name),'w') as f:
        for c in counter:
            f.write('%s\t%d\n'%c)
            

def continuous_category(variable):
    raw_values=open(r'%s\c\%s.txt'%(date,variable.name)).read().split('\n')[:-1]
    values=[float(v) for v in raw_values]

    categorys=[]
    for i in range(len(values)-1):
        category=Category()
        category.id=i
        category.name='['+str(values[i+1])+','+str(values[i])+')'
        category.ceiling=values[i]
        category.floor=values[i+1]
        category.alpha=[]
        for d in data:
            try:
                if values[i+1]<float(d[variable.col])<values[i]:
                    stock=d[0]
                    start_date=shift_date(d[1])
                    end_date=shift_date(start_date,0) #notice that the parameter should be 0
                    category.alpha.append((stock,start_date,end_date,1))
            except:
                pass
        category.avg_return=alpha_to_avg_alpha_return(category.alpha)
        
        categorys.append(category)
        print values[i]
    return categorys


def discrete_category(variable):
    raw_values=open(r'd\%s.txt'%variable.name).read().split('\n')[:-1]
    #some categorys' sample is too small,a threshold(100) is set,
    #means that we just observe those category with samples more than 100
    values=[v.split('\t')[0] for v in raw_values if int(v.split('\t')[1])>100]
    
    categorys=[]
    for i in range(len(values)):
        category=Category()
        category.id=i
        category.name=values[i]
        category.alpha=[]
        for d in data:
            if d[variable.col]==values[i]:
                stock=d[0]
                start_date=shift_date(d[1])
                end_date=shift_date(start_date,0)
                category.alpha.append((stock,start_date,end_date,1))
    
        category.avg_return=alpha_to_avg_alpha_return(category.alpha)
        
        categorys.append(category)
        print values[i]
    return categorys


def get_grades(window_data,target_data,variables):
    global data,date
    data=window_data
    date=target_data[1]
    
    grades=[]
    for variable in variables:
        if variable.datatype=='c':
            statistic_continuous_variable(variable)
            categorys=continuous_category(variable)
            for category in categorys:
                if category.floor<=target_data[variable.col]<category.ceiling:
                    grades.append(category.avg_return)
                    break
        elif variable.datatype=='d':
            statistic_discrete_variable(variable)
            categorys=discrete_category(variable)
            for category in categorys:
                if category.name==target_data[variable.col]:
                    grades.append(category.avg_return)
                    break
    return grades
    
    