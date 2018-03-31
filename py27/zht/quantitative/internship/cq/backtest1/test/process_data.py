# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 15:26:27 2016

@author: hp
"""
import os

lines=open('data_description.txt').read().split('\n')[:-1]
colnames=[tuple(l.split('\t')) for l in lines]

class Variable:
    def __init__(self,name,col,datatype):
        self.name=name
        self.col=int(col)
        self.datatype=datatype
        


def process_continuous_variable(variable):
    variable.interval_number=5
    lines=open('data.txt').read().split('\n')[:-1]
    
    raw_values=[]
    for l in lines:
        #some values may be invalid,this will skip those values
        try:
            raw_values.append(float(l.split('\t')[variable.col]))
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
    




def process_discrete_variable(variable):
    lines=open('data.txt').read().split('\n')[:-1]
    values={}
    for l in lines:
        value=l.split('\t')[variable.col]
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
    variables=[Variable(colnames[i][0],colnames[i][1],colnames[i][2]) for i in range(len(colnames))]
    for variable in variables:
        if variable.datatype=='c':
            process_continuous_variable(variable)
        elif variable.datatype=='d':
            process_discrete_variable(variable)
        

if __name__=='__main__':
    run()



