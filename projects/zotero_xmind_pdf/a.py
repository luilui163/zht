# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-01  22:27
# NAME:zht-base_on_foxit.py
import sqlite3
import sys
import os
import re
import pandas as pd
from webcolors import rgb_to_hex

with open(r'e:\a\foxit.fdf',encoding='utf8',errors='ignore') as f:
    lines=f.readlines()

lines=[l for l in lines if 'Contents' in l]


color_list=l.split(']')[0].split('[ ')[-1].split(' ')
color = rgb_to_hex(list(int(round(float(c) * 255)) for c in color_list))

text=l.split('Annot/Contents(')[-1].split(')/CA')[0]
text = _filter_text(text)

rect=l.split(']/F')[0].split('Rect[ ')[-1].split(' ')
left, bottom, right, top = (float(r) for r in rect)

_type=l.split('Subtype/')[-1].split('/Type')[0].lower()
page=int(l.split('/RC')[0].split('/Page ')[-1])

print(page,_type,color_list,rect,text)




