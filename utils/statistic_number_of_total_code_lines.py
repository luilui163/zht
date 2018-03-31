# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 21:52:15 2016

@author: hp
"""

import os 
import os.path
rootdir=r'C:\Anaconda\zht'

filepaths=[]
for parent,dirnames,filenames in os.walk(rootdir):
#    for dirname in dirnames:
#        print 'parent is:',parent
#        print 'dirname is:',dirname
    
    for filename in filenames:
#        print 'parent is:',parent
#        print 'filename is:',filename
        filepath=os.path.join(parent,filename)
        print('the full name of the file is:',filepath)
        filepaths.append(filepath)
python_file=[fp for fp in filepaths if fp.endswith('py')]
print(len(python_file))



count=0
for pf in python_file:
    with open(pf) as f:
        for line in f:
            if line.split():
                count+=1
print(count)





