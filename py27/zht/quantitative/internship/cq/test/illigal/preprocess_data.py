# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 16:29:56 2016

@author: hp
"""

import util

def run():
    lines=open('data.txt').read().split('\n')[:-1]
    new_lines=[]
    for i in range(2,len(lines)):
        if i<2:
            new_lines.append(lines[i])
        else:
            items=lines[i].split('\t')
            items[0]=util.normalize_sid(items[0])
            items[1]=util.normalize_date(items[1])
            new_lines.append('\t'.join(items))
    
    with open('data.txt','w') as f:
        for l in lines:
            f.write(l+'\n')

