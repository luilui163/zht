# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 10:05:37 2016

@author: 13163
"""
import os

def initialize_concept_name_file():
    dir_name=r'c:\cq\concept\wind'
    file_names=os.listdir(dir_name)
    file_paths=[os.path.join(dir_name,file_name) for file_name in file_names]
    concept_names=[]
    fp=file_paths[0]
    lines=open(fp).read().split('\n')[:-1]
    for l in lines:
        concepts_str=l.split('\t')[1]
    #    line_concepts=concepts_str.split(';') if ';' in concepts_str else concepts_str
        line_concepts=concepts_str.split(';')
        for lc in line_concepts:
            if lc not in concept_names:
                concept_names.append(lc)
    f=open(r'c:\cq\concept\wind_formatted\concept_name.txt','w')
    code=1
    for cn in concept_names:
        f.write('%d\t%s\n'%(code,cn))
        code+=1
    f.close()

def update_concept_name_file(date_path):
    old_lines=open(r'c:\cq\concept\wind_formatted\concept_name.txt').read().split('\n')[:-1]
#    code_list=[ol.split('\t') for ol in old_lines]
    concept_names=[ol.split('\t')[1] for ol in old_lines]
    
    
    lines=open(date_path).read().split('\n')[:-1]
    for l in lines:
        concepts_str=l.split('\t')[1]
    #    line_concepts=concepts_str.split(';') if ';' in concepts_str else concepts_str
        line_concepts=concepts_str.split(';')
        for lc in line_concepts:
            if lc not in concept_names:
                concept_names.append(lc)
    
    f=open(r'c:\cq\concept\wind_formatted\concept_name.txt','w')
    code=1
    for cn in concept_names:
        f.write('%d\t%s\n'%(code,cn))
        code+=1
    f.close()

def f():
    dir_name=r'c:\cq\concept\wind'
    file_names=os.listdir(dir_name)
    file_paths=[os.path.join(dir_name,file_name) for file_name in file_names]
    
    initialize_concept_name_file()
    for fp in file_paths[1:]:
        update_concept_name_file(fp)
        print fp


def change_type():
    dir_name=r'c:\cq\concept\wind'
    file_names=os.listdir(dir_name)
    file_paths=[os.path.join(dir_name,fn) for fn in file_names]

    concept_name=open(r'C:\cq\concept\wind_formatted\concept_name.txt').read().split('\n')[:-1]
    code=[cn.split('\t')[0] for cn in concept_name]
    name=[cn.split('\t')[1] for cn in concept_name]
    
    for fp in file_paths:
        lines=open(fp).read().split('\n')[:-1]
        date=fp[-12:-4]
        new_f=open(r'C:\cq\concept\wind_formatted\data\%s.txt'%date,'w')
        for l in lines:
            stock=l.split('\t')[0]
            if stock[-1]=='H':
                new_stock=stock[:-1]+'S'
            else:
                new_stock=stock
            concepts=l.split('\t')[1].split(';')
            concept_code=[code[name.index(c)] for c in concepts]
            new_f.write('%s\t%s\n'%(new_stock,'\t'.join(concept_code)))
        new_f.close()
    


f()
change_type()









