# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-01  22:27
# NAME:zht-base_on_foxit.py


from pdfrw import PdfReader, PdfWriter



fp=r'e:\a\Yan and Zheng - 2017 - Fundamental Analysis and the Cross-Section of Stoc.pdf'
fpn=r'e:\a\new.pdf'

trailer = PdfReader(fp)

trailer.Info.Title = 'My New Title Goes Here'

PdfWriter(fpn, trailer=trailer).write()


content=trailer.read_all()

import reportlab
