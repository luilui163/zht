# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 16:01:30 2016

@author: Administrator
"""

import os 


path=r'c:\bloomberg_new\timing'
files=os.listdir(path)
files_paths=[os.path.join(path,f) for f in files]

files_paths=sorted(files_paths,key=lambda x:x[-12:-4])
f=open(r'c:\bloomberg_new\timing.txt','w')
for i in range(len(files_paths)):
    lines=open(files_paths[i]).read().split('\n')
    f.write('%s\t%s\n'%(files_paths[i][-12:-4],lines[0]))
f.close()