# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 15:25:11 2016

@author: Administrator
"""
import os

path=r'c:\cq\concept\wind'
file_names=os.listdir(path)
file_paths=[os.path.join(path,f) for f in file_names]

def get_concepts(file_path):
    special_char=['*','?','“','<','>','|']
    
    lines=open(file_path).read().split('\n')[:-1]
    concepts=[]
    for l in lines:
        tmp=l.split('\t')[1].split(';')
        for t in tmp:
            if t not in concepts:
                #由于文件名不能包含special_char这些特殊字符，这里把它们去掉
                #不能这样，因为有的概念名为*ST有的为ST，这样就把两个概念弄到一起去了
                for s in special_char:
                    if s in t:
                        t=t.replace(s,'')
                concepts.append(t)
    return concepts

for i in range(len(file_names)):
    date=file_names[i][:-4]
    date_dir=r'c:\cq\concept\concepts\%s'%date
    if not os.path.isdir(date_dir):
        os.makedirs(date_dir)
    concepts=get_concepts(file_paths[i])
    for c in range(len(concepts)):
        f=open(os.path.join(date_dir,concepts[c]+'.txt'),'w')
        lines=open(file_paths[i]).read().split('\n')[:-1]
        for l in lines:
            if ';' in l.split('\t')[1]:
                belong_concepts=l.split('\t')[1].split(';')
            else:
                belong_concepts=l.split('\t')[1]
            if concepts[c] in belong_concepts:
                f.write('%s\n'%l.split('\t')[0])
        f.close()
    print date

