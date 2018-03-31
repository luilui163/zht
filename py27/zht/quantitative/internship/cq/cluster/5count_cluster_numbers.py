# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 09:55:05 2016

@author: Administrator
"""
import os
from pyExcelerator import *

'''
def get_number_of_clusters(directory):
    w=Workbook()
    ws=w.add_sheet('number_of_clusters')
    dates=os.listdir(directory)
    for m in range(len(dates)):
        ws.write(0,m,dates[m])
        
        path=directory+'\\'+dates[m]
        files=os.listdir(path)
        files_paths=[os.path.join(path,f) for f in files]
        numbers=[0]*len(files_paths)
        for j in range(len(files_paths)):
            numbers[j]=len(open(files_paths[j]).read().split('\n')[:-1])
        numbers=sorted(numbers,reverse=True)
        for i in range(len(files_paths)):
            ws.write(i+1,m,numbers[i])
    w.save(r'c:\cluster\number\%s.xls'%directory.split('\\')[-1])
'''





def get_number_of_clusters(directory):
    w=Workbook()
    ws=w.add_sheet('number_of_clusters')
    file_name=os.listdir(directory)
    date=[f[:-4] for f in file_name]
    for m in range(len(date)):
        ws.write(0,m,date[m])
        path=directory+'\\'+file_name[m]
        lines=open(path).read().split('\n')[:-1]
        category=list(set([l.split('\t')[1] for l in lines]))
        numbers=[0]*len(category)
        for n in range(len(numbers)):
            for j in range(len(lines)):
                if lines[j].split('\t')[1]==category[n]:
                    numbers[n]+=1

        numbers=sorted(numbers,reverse=True)
        for i in range(len(numbers)):
            ws.write(i+1,m,numbers[i])
        w.save(r'c:\cluster\number\%s.xls'%directory.split('\\')[-1])
                    
directory=r'C:\Users\Administrator\Desktop\hierarchical_cluster\fourth'
get_number_of_clusters(directory)          
                    
                    