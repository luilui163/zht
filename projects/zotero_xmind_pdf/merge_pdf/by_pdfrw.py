# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-10-19  23:23
# NAME:zht-by_pdfrw.py


import sys
import os

from pdfrw import PdfReader, PdfWriter, IndirectPdfDict


directory=r'E:\a\test_pdfminer'

fns=os.listdir(directory)

outfn=os.path.join(directory,'output.pdf')

writer = PdfWriter()
for inpfn in fns:
    writer.addpages(PdfReader(os.path.join(directory,inpfn)).pages)

writer.trailer.Info = IndirectPdfDict(
    Title='your title goes here',
    Author='your name goes here',
    Subject='what is it all about?',
    Creator='some script goes here',
)
writer.write(outfn)
