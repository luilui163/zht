# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:27:48 2016

@author: hp
"""
import os
from WindPy import *
from datetime import *
import pandas as pd
import time
w.start()


data=w.wset("managersalarystat","year=2014;sectorid=a001010100000000")
d=data.Data
date=d[-1][0].strftime('%Y%m%d')
f=open(r'c:\cq\manage_salary\%s.txt'%date,'w')
f.write('wind_code\tthree_directors_compensation\tthree_managers_compensation\tother_treatment\n')

def change_code(code):
    if code[-1]=='H':
        return code[:-1]+'S'
    else:
        return code

wind_code=map(change_code,wind_code)
three_directors_compensation=d[2]
three_managers_compensation=d[3]
other_treatment=d[4]
#report_date=d
for i in range(len(wind_code)):
    f.write(wind_code[i])
    f.write('\t')
    f.write(str(three_directors_compensation[i]))
    f.write('\t')
    f.write(str(three_managers_compensation[i]))
    f.write('\t')
    f.write(str(other_treatment[i]))
    f.write('\n')
    print i
f.close()
