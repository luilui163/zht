# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-09-09  15:45
# NAME:zht-merge_pdf.py



import os

from PyPDF2 import PdfFileMerger,PdfFileReader

'''
merge pdfs by using smallpdf, refer to 
https://smallpdf.com/merge-pdf

use pdfmerger.jar  (github)
'''

def by_pdfrw():
    '''
    The problem with this package is that the bookmarks can not be conveyed
    to the new combined pdf.

    :return:
    '''
    import os
    from pdfrw import PdfReader, PdfWriter, IndirectPdfDict

    directory = r'E:\a\test_pdfminer'

    fns = os.listdir(directory)

    outfn = os.path.join(directory, 'output.pdf')

    writer = PdfWriter()
    for inpfn in fns:
        writer.addpages(PdfReader(os.path.join(directory, inpfn)).pages)

    writer.trailer.Info = IndirectPdfDict(
        Title='your title goes here',
        Author='your name goes here',
        Subject='what is it all about?',
        Creator='some script goes here',
    )
    writer.write(outfn)



fns=os.listdir(r'E:\a\tag_China\files')

pdfs=[]
for dp,dn,fns in os.walk(r'E:\a\tag_China\files'):
    for fn in fns:
        if fn.endswith('.pdf'):
            old_path=os.path.join(dp,fn)
            new_path=os.path.join(dp,fn).replace(' ','').replace(',','')
            os.rename(old_path,new_path)
            pdfs.append(new_path)

# merger=PdfFileMerger()
#
# sucess=0
# fail=0
# for pdf in pdfs:
#     try:
#         pdfFile=PdfFileReader(pdf)
#         if pdfFile.isEncrypted:
#             pdfFile.decrypt('')
#         merger.append(pdfFile)
#         sucess+=1
#     except:
#         print(os.path.basename(pdf))
#         fail+=1
#
# print(sucess,fail)
#
# with open(r'e:\a\result.pdf','wb') as f:
#     merger.write(f)

from PyPDF2 import PdfFileMerger

merger = PdfFileMerger()

pdfs=pdfs[:10]#fixme:


i=0
for pdf in pdfs:
    try:
        print(pdf)
        with open(pdf,'rb') as con:
            merger.append(con)
        # merger.append(open(pdf, 'rb'))
        i+=1
    except:
        pass

print(i)
with open(r'e:\a\result.pdf', 'wb') as fout:
    merger.write(fout)


print(i)


