# -*- coding: utf-8 -*-
"""
Created on Thu Jul 07 11:11:30 2016

@author: 13163
"""
import os

dir_name=r'C:\cq\concept\wind_formatted\data'
file_names=os.listdir(dir_name)
dates=[fn[:-4] for fn in file_names]
file_paths=[os.path.join(dir_name,fn) for fn in file_names]
cn=open(r'C:\cq\concept\wind_formatted\concept_name.txt').read().split('\n')[:-1]
concept_name=[cnn.split('\t')[1] for cnn in cn]
concept_code=[cnn.split('\t')[0] for cnn in cn]


for fp in file_paths:
    lines=open(fp).read().split('\n')[:-1]
    fp_concepts=[]
    for l in lines:
        l_concepts=l.split('\t')[1:]
        for lc in l_concepts:
            if lc not in fp_concepts:
                fp_concepts.append(lc)
    fp_concepts_count=[]
    for fp_concept in fp_concepts:
        tmp_counter=0
        for l in lines:
            if fp_concept in l.split('\t')[1:]:
                tmp_counter+=1
        fp_concepts_count.append(tmp_counter)
    avg=sum(fp_concepts_count)*1.0/len(fp_concepts_count)
    minimum=min(fp_concepts_count)
    maximum=max(fp_concepts_count)
    
    fp_concepts_name=[concept_name[concept_code.index(fc)] for fc in fp_concepts]
#    z=zip(fp_concepts_name,fp_concepts_count)
    z=zip(fp_concepts_count,fp_concepts_name)
    sorted_z=sorted(z,key=lambda s:s[0])
    f=open(r'C:\cq\concept\wind_formatted\count\%s.txt'%fp[-12:-4],'w')
    f.write('number\t%d\n'%len(fp_concepts_count))
    f.write('avg\t%f\n'%avg)
    f.write('min\t%d\n'%minimum)
    f.write('max\t%d\n\n'%maximum)
    for m in sorted_z:
        f.write('%d\t%s\n'%m)
    f.close()
    print fp
    
        

