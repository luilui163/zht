#-*-coding: utf-8 -*-
#author:tyhj
#a.py 2017/9/3 15:06
import pandas as pd
import numpy as np

import os

path=r'D:\quantDb\sourceData\gta\data'

df=pd.read_csv(os.path.join(path,'menuNew1.csv'))

names=['dbname','DBTitle','NoteTitle','TBTitle','Title']
newdf=df[names]

with open(os.path.join(path,'html.html'),'w') as f:
    f.write('<table id="mytable">')

    for i in range(newdf.shape[0])[:10]:
        for j in range(newdf.shape[1]):
            p='''
            <tr data-depth="%s" class="collapse level%s">
            <td><span class="toggle collapse"></span>%s</td>
            </tr>
            '''%(j,j,newdf.iloc[i,j])
            f.write(p+'\n')
        print i
    f.write('</table>')

print 'finished'


