#-*-coding: utf-8 -*-
#author:tyhj
#cleanOutputDirectory.py 2017.11.8 13:57
import os
import shutil
path=r'D:\blog\pelican9\output'

fns=os.listdir(path)
toDelete=[fn for fn in fns if fn != '.git']
for fn in toDelete:
    element=os.path.join(path,fn)
    if os.path.isdir(element):
        shutil.rmtree(element)
    elif os.path.isfile(element):
        os.remove(element)














