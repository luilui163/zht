# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 14:59:40 2016

@author: 13163
"""

import pandas as pd
import os

file_dir=r'c:\cq\concept\wind_formatted\data'
file_name=os.listdir(file_dir)
file_path=[os.path.join(file_dir,fn) for fn in file_name]
date=[fn[:-4] for fn in file_name]


def get_target_data(i):
#i=1
    lines0=open(file_path[i-1]).read().split('\n')[:-1]
    lines1=open(file_path[i]).read().split('\n')[:-1]
    stocks0=[l.split('\t')[0] for l in lines0]
    stocks1=[l.split('\t')[0] for l in lines1]
    target_stocks=[]
    initial_concept=[]
    target_concept=[]
    intersection_stock=[s1 for s1 in stocks1 if s1 in stocks0]
    for s in intersection_stock:
        mark=0
        index1=stocks1.index(s)
        concepts1=lines1[index1].split('\t')[1:]
        index0=stocks0.index(s)
        concepts0=lines0[index0].split('\t')[1:]
        tmp_concept=[]
        for c1 in concepts1:
            if c1 not in concepts0:
                tmp_concept.append(c1)
                mark=1
        if mark==1:
            target_stocks.append(s)
            initial_concept.append(concepts0)
            target_concept.append(tmp_concept)
    
    return target_stocks,initial_concept,target_concept

def get_signal_file():
    path=r'c:\garbage\concept\signal'
    if not os.path.isdir(path):
        os.makedirs(path)
    for i in range(1,len(date)):
        target_stocks,initial_concept,target_concept=get_target_data(i)
        if target_stocks!=[]:
            f=open(os.path.join(path,date[i]+'.txt'),'w')
            for t in range(len(target_stocks)):
                f.write(target_stocks[t]+'-'+'\t'.join(initial_concept[t])+'-'+'\t'.join(target_concept[t])+'\n')
            f.close()
            print date[i]

if __name__=='__main__':
    get_signal_file()
    