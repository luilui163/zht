#-*-coding: utf-8 -*-
#author:tyhj
#c.py 2017/9/18 16:09


#TODO:wrong!!!!!!


year = month[:4]
validmonths = [year + '-0' + str(i) for i in range(7, 10)]
validmonths += [year + '-1' + str(i) for i in range(3)]
validmonths += [str(int(year) + 1) + '-0' + str(i) for i in range(1, 7)]








