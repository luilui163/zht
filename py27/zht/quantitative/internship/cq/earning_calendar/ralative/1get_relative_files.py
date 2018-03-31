# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 13:33:19 2016

@author: Administrator
"""
import os
import shutil

path=r'C:\earning_calendar\quarter'
files=os.listdir(path)
files_paths=[os.path.join(path,f) for f in files]
for i in range(len(files_paths)):
    if files_paths[i][-5]=='1':
        shutil.copyfile(files_paths[i],r'c:\earning_calendar\relative\Q1\%s'%files[i])
    elif files_paths[i][-5]=='2':
        shutil.copyfile(files_paths[i],r'c:\earning_calendar\relative\Q2\%s'%files[i])
    elif files_paths[i][-5]=='3':
        shutil.copyfile(files_paths[i],r'c:\earning_calendar\relative\Q3\%s'%files[i])
    elif files_paths[i][-5]=='4':
        shutil.copyfile(files_paths[i],r'c:\earning_calendar\relative\Q4\%s'%files[i])




