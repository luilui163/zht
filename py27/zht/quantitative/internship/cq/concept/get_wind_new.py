# -*- coding: utf-8 -*-
"""
Created on Mon Jul 04 10:11:14 2016

@author: 13163
"""

import os
dir_path=r'c:\cq\concept\concepts'
date=os.listdir(dir_path)
date_dir=[os.path.join(dir_path,d) for d in date]

for dd in date_dir:
    new_dir=r'c:\cq\concept\wind_new\%s'%dd[-8:]
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)
    file_name=os.listdir(dd)
    file_path=[os.path.join(dd,f) for f in file_name]
    for i in range(len(file_path)):
        content=open(file_path[i]).read()
        f=open(os.path.join(new_dir,file_name[i]),'w')
        f.write(content.replace('.SZ','').replace('.SH',''))
        f.close()
    print dd



#path=r'c:\garbage\ST.txt'
#lines=open(path).readlines()
#f=open(r'c:\garbage\ST1.txt','w')
#for l in lines:
#    f.write(l.replace('.SZ','').replace('.SH',''))
#f.close()

