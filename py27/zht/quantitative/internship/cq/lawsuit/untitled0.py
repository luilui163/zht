# -*- coding: utf-8 -*-
"""
Created on Fri Aug 05 10:31:28 2016

@author: hp
"""

import pandas as pd
import numpy as np
import os
import re
import json


announcement_date_df=pd.read_csv(R'c:\cq\announcement_date.csv',index_col=0)
std_stock=list(announcement_date_df.columns)
#f_report=open(R'c:\cq\lawsuit\report_accuser.txt','w')
#f_out_report=open(r'c:\cq\lawsuit\out_report_accuser.txt','w')

def in_or_out_report():
    in_report=[]
    out_report=[]
    src=r'c:\cq\lawsuit\lawsuit'
    file_name=os.listdir(src)
    file_name.sort(lambda a,b:int(a.split('.')[0])-int(b.split('.')[0]))
    file_path=[os.path.join(src,fn) for fn in file_name]
    for fp in file_path:
        date=int(fp[-12:-4])
        lines=open(fp).read().split('\n')[:-1]
        for l in lines:
            stock=l.split('|')[0].replace('SH','SS')
            content=l.split('|')[1]
            js=json.loads('{'+content+'}')
            suit_name=js['col2']
            accuser=js['col4']
            accused=js['col5']
            suit_type=js['col6']
            suit_date=js['col8'].replace('-','')
            amount=js['col9']
            judgement_date=js['col11']
            sue=js['col13']
            if stock in std_stock:
                report_date_list=list(announcement_date_df[stock])
                if date in report_date_list:
                    in_report.append((stock,suit_name,accuser,accused,suit_type,suit_date,amount,judgement_date,sue))
    #                f_report.write('\t'.join([stock,suit_name,accuser,accused,suit_type,suit_date,amount,judgement_date,sue])+'\n')
                else:
                    out_report.append((stock,suit_name,accuser,accused,suit_type,suit_date,amount,judgement_date,sue))
    #                f_out_report.write('\t'.join([stock,suit_name,accuser,accused,suit_type,suit_date,amount,judgement_date,sue])+'\n')
    return in_report,out_report

in_report,out_report=in_or_out_report()


































