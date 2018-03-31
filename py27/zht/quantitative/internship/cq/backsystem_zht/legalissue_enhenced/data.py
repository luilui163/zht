# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 13:54:25 2016

@author: hp
"""


'''
注意还要删除重复的ticker，因为有的案例出了处罚对象不同，别的都是相同的
但是，处罚对象这个变量在处理数据的时候都删了，所以，会有完全重复的样本。
'''
import os
import csv

file_dir=r'C:\Users\hp\Desktop\legalissue\data'
file_name=os.listdir(file_dir)
file_path=[os.path.join(file_dir,fn) for fn in file_name]

title=[]
data=[]
for m in range(2005,2017):
    fp=r'C:\Users\hp\Desktop\legalissue\data\%d.csv'%m
    with open(fp) as f:
        lines=csv.reader(f)
        for n,line in enumerate(lines):
            if n==1:
                title=line
            if n>=2:
                if line[0]=='':
                    break
                data.append(line)
    print m


del title[8]
del title[6]
del title[1]
for d in data:
    del d[8]
    del d[6]
    del d[1]

    
with open(r'raw_data1.txt','w') as f:
    f.write('\t'.join(title)+'\n')
    for d in data:
        f.write('\t'.join(d)+'\n')

#with open('raw_data4.csv','w') as f:
#    writer=csv.writer(f)
#    writer.writerow(title)
#    writer.writerows(data[:10])
    
content=open(r'C:\Users\hp\Desktop\legalissue\raw_data1.txt').read()
content=content.replace('\n\n','\n')
with open(r'C:\Users\hp\Desktop\legalissue\raw_data2.txt','w') as f:
    f.write(content)

import re
pat=re.compile('\d\d\d\d\d\d')
lines=open(r'c:\users\hp\desktop\legalissue\raw_data2.txt').read().split('\n')[:-1]
valid_lines=[]
for line in lines:
    #there is some sample not in regular data form
    if re.match(pat,line):
        valid_lines.append(line)
    else:
        if len(valid_lines)>0:
            del valid_lines[-1]

with open(r'c:\users\hp\desktop\legalissue\raw_data3.txt','w') as f:
    for l in valid_lines:
        f.write(l+'\n')