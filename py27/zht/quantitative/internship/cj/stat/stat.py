#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
import os
import re
import xlrd

path=u'C:\\data\\cj\\stat\\test\\2016年12月'.encode('gbk')
filenames=os.listdir(path)
f=[fn for fn in filenames if not fn.startswith('0')][0]
filenames=[fn for fn in filenames if fn.startswith('0')]


# df=pd.read_excel(os.path.join(path,fund))
#
# with pd.ExcelWriter('test.xls') as writer:
#     df.to_excel(writer,sheet_name=str(0))


bk=xlrd.open_workbook(os.path.join(path,f))
sheetnames=bk.sheet_names()
# sheetnames=[sn.encode('gbk') for sn in sheetnames]

sheetname=[s for s in sheetnames if s.startswith('F2')][0]

table=bk.sheet_by_name(sheetname)

for rownum in range(table.nrows):
    print table.row_values(rownum)























