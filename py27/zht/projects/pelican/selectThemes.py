#-*-coding: utf-8 -*-
#author:tyhj
#selectThemes.py 2017.11.5 10:29
import os

path=r'D:\blog\pelican9\pelican-themes'

themes=os.listdir(path)
themes=filter(lambda x:os.path.isdir(os.path.join(path,x)),os.listdir(path))
themes=[t for t in themes if not t.startswith('.')]

invalidThemes=[t for t in themes if not os.listdir(os.path.join(path,t))]
validThemes=[t for t in themes if os.listdir(os.path.join(path,t))]
for t in invalidThemes:
    os.rmdir(os.path.join(path,t))
with open('validThemes.txt','w') as f:
    for t in validThemes:
        f.write(t+'\n')













