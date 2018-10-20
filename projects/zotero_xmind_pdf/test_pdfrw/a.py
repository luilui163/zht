# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-10-19  23:29
# NAME:zht-a.py

from pdfrw import PdfReader,PdfFileReader

import os

directory=r'E:\a\test_pdfminer'

fns=os.listdir(directory)

fn=fns[0]

# x=PdfReader(os.path.join(directory,fn))

