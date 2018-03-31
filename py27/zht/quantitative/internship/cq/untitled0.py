# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 15:00:34 2016

@author: hp
"""

import codecs

str1=u'这是一个str'
for ch in str1:
    print ch
f=open(r'c:\garbage\test.txt','w')
f.write(str1.encode('gbk'))
f.close()
