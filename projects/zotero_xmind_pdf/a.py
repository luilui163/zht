# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-01  22:27
# NAME:zht-base_on_foxit.py
import sqlite3
import sys
import os
import re

path1=r'E:\a\DEMO Food Quality - A Global Challenge (2)\DEMO Food Quality - A Global Challenge (2).sqlite'

import zipfile

# zip_ref=zipfile.ZipFile(path,'r')
# zip_ref.extractall(r'e:\a\test_ctv')
# zip_ref.close()

import magic



conn=sqlite3.connect(path1)

c=conn.cursor()

q='select * from annotation'

c.execute(q)

items=c.fetchall()

item=items[0]

item[0].decode('windows-1251')


import chardet

chardet.detect(item[0])
