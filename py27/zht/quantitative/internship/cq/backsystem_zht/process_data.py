# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 15:26:27 2016

@author: hp
"""
import os
from util import *

def preprocess_data():
    with open('raw_data.txt') as f:
        lines=f.read().split('\n')[:-1]
    new_lines=[]
    new_lines.append(lines[0])
    tmp_l=[]
    for i in range(len(lines[0].split('\t'))):
        tmp_l.append('v'+str(i))
    new_lines.append('\t'.join(tmp_l))
    new_lines.append(lines[1])
    
    data=[]
    for i in range(2,len(lines)):
        items=lines[i].split('\t')
        items[0]=normalize_sid(items[0])
        items[1]=normalize_date(items[1])
        #if sid is not in reuturn_df_stocks,items[0] is None
        if items[0]!=None:
            data.append(items)
        else:
            pass
    data.sort(key=lambda x:int(x[1]))
    
    new_lines+=['\t'.join(d) for d in data]
    
    with open('data.txt','w') as f:
        for l in new_lines:
            f.write(l+'\n')
    
    with open('data_description.txt','w') as f:
        name_raw=new_lines[0].split('\t')
        name=new_lines[1].split('\t')
        datatype=new_lines[2].split('\t')
        zp=zip(name,datatype,name_raw)
        f.write('name\tdatatype\tname_raw\n')
        for z in zp:
            f.write('%s\t%s\t%s\n'%z)

class Variable:
    def __init__(self,name_raw,name,datatype,col):
        self.name_raw=name_raw
        self.name=name
        self.datatype=datatype
        self.col=int(col)

def process_continuous_variable(data,variable):
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
    
    if not os.path.isdir('c'):
        os.makedirs('c')
        
    with open(r'c\%s.txt'%variable.name,'w') as f:
        for value in variable.values:
            f.write('%f\n'%value)
    


def process_discrete_variable(data,variable):
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
    
    with open('d\%s.txt'%variable.name,'w') as f:
        for c in counter:
            f.write('%s\t%d\n'%c)

def run():
    preprocess_data()
    
    dd=open(r'data.txt').read().split('\n')[:-1]
    name_raw=dd[0].split('\t')
    name=dd[1].split('\t')
    datatype=dd[2].split('\t')
    data=[r.split('\t') for r in dd[3:]]
    title=zip(name_raw,name,datatype,range(len(name_raw)))

    variables=[Variable(t[0],t[1],t[2],t[3]) for t in title if t[2] in ['c','d']]
    for variable in variables:
        if variable.datatype=='c':
            process_continuous_variable(data,variable)
        elif variable.datatype=='d':
            process_discrete_variable(data,variable)
        

if __name__=='__main__':
    run()


