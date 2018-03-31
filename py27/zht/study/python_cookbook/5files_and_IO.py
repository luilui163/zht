# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 14:24:53 2016

@author: hp
"""

#Iterating over fixed-sized records

from functools import partial

RECORD_SIZE=32
with open('somefile.data','rb') as f:
    records=iterpartial(f.readd(),RECORD_SIZE)),'b')
    for r in records:
        pass
