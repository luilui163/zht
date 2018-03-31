#-*-coding: utf-8 -*-
#author:tyhj
#scanSpecialWebsites.py 2017/8/19 22:02

from io import *
from urllib import *
from string import *

def urliter():
    for i in xrange(100):
        print '%d/100' %i
        for j in lowercase:
            for k in lowercase:
                yield 'http://www.%02d%c%c%c%c.com'%(i,j,k,j,k)

with open(r'e:\aa\findsomewebsites.txt','w') as f:
    for u in urliter():
        try:
            wp=urlopen(u)
            print u
            f.write(u+'\n')
        except:
            pass











