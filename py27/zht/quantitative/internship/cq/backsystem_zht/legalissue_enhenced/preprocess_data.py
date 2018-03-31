# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 16:29:56 2016

@author: hp
"""
from util import *
def run():
    with open('raw_data.txt') as f:
        lines=f.read().split('\n')[:-1]
    new_lines=[]
    new_lines.append(lines[0])
    tmp_l=[]
    for i in range(len(lines[0].split('\t'))):
        tmp_l.append('v'+str(i))
    new_lines.append('\t'.join(tmp_l))
    new_lines.append(lines[1])
    for i in range(2,len(lines)):
        items=lines[i].split('\t')
        items[0]=normalize_sid(items[0])
        items[1]=normalize_date(items[1])
        #if sid is not in reuturn_df_stocks,items[0] is None
        if items[0]!=None:
            new_lines.append('\t'.join(items))
        else:
            pass
    
    with open('data.txt','w') as f:
        for l in new_lines:
            f.write(l+'\n')
    
    with open('data_description.txt','w') as f:
        name_raw=new_lines[0].split('\t')
        name=new_lines[1].split('\t')
        datatype=new_lines[2].split('\t')
        zp=zip(name,datatype,name_raw)
        f.write('name\tdatatype\tname_raw\n')
        for z in zp:
            f.write('%s\t%s\t%s\n'%z)

if __name__=='__main__':
    run()