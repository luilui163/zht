#-*-coding: utf-8 -*-
#@author:tyhj

import os
import calendar

def unify_filenames():
    path=r'C:\data\barra_factors'
    for dirpath,dirnames,filenames in os.walk(path):
        for filename in filenames:
            if int(filename[-6:-4])<20:
                os.remove(os.path.join(dirpath,filename))
            else:
                year = filename[:4]
                month = filename[5:7]
                new_date = year + '-' + month + '-' + str(calendar.monthrange(int(year), int(month))[1])
                os.rename(os.path.join(dirpath,filename), os.path.join(dirpath, new_date + '.csv'))




if __name__=='__main__':
    unify_filenames()








