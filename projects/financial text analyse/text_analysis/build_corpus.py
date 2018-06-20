# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-06-18  16:02
# NAME:zht-build_corpus.py
import multiprocessing

from Scripts.pdf2txt import extract_text
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os

from utils.dateu import get_current_time
from utils.sysu import multiProcess, monitor

directory_pdf=r'D:\zht\database\zoteroDB\storage'
directory_txt=r'D:\zht\database\projects\financial_paper_corpus'



def by_PyPDF2():
    path = r'E:\a\Stambaugh and Yuan - 2016 - Mispricing factors.pdf'

    import PyPDF2

    pdfReader=PyPDF2.PdfFileReader(open(path,'rb'))
    pages=pdfReader.getNumPages()

    for page in range(pages):
        print(pdfReader.getPage(page).extractText())

def pdf2txt_0(path):
    name=os.path.basename(path)[:-4]
    print(get_current_time(),name)
    extract_text([path],outfile=os.path.join(directory_txt,name+'.txt'))

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for i,page in enumerate(PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True)):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text.replace('\n','')

def task(path):
    print(path)
    name=os.path.basename(path)[:-4]
    text=convert_pdf_to_txt(path)
    with open(os.path.join(directory_txt,name+'.txt'),'w',encoding='utf8') as f:
        f.write(text)

if __name__ == '__main__':
    x = [os.path.join(r, file) for r, d, f in os.walk(directory_pdf) for file in f]
    paths = [f for f in x if f.endswith('.pdf')]
    parsed=os.listdir(directory_txt)
    paths=[p for p in paths if os.path.basename(p)[:-4] not in [a[:-4] for a in parsed]]
    pool = multiprocessing.Pool(6)
    pool.map(pdf2txt_0,paths)











