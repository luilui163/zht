# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 18:00:28 2016

@author: Administrator
"""
import os
path=r'c:\earning_calendar\quarter'
files=os.listdir(path)
filesPath=[os.path.join('%s\%s'%(path,f)) for f in files]
for i in range(len(filesPath)):
    f=open(r'c:\earning_calendar\quarter1\%s'%files[i],'w')
    line=open(filesPath[i]).read().split('\n')[:-1]
    for j in range(len(line)):
        if line[j][-1]=='S':
            f.write('%sH\n'%line[j][:-1])
        else:
            f.write('%s\n'%line[j])
    f.close()