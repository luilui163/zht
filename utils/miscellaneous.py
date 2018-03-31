# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 12:02:44 2016

@author: hp
"""

from io import *
from string import *
from string import ascii_lowercase
from urllib.request import urlopen


def urliter() :
    for i in range(100) :
        print("%d/100"  % i)
        for j in ascii_lowercase :
            for k in ascii_lowercase :
                yield "http://www.%02d%c%c%c%c.com" % (i, j, k, j, k)

logfile = open("findsomewebsites.log", "w")

for u in urliter() :
    try :
        wp = urlopen(u)
        print("find " + u)
        logfile.write(u + "\n")
    except :
        pass

logfile.close()

