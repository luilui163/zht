# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-06-18  16:02
# NAME:zht-build_corpus.py
import multiprocessing

from Scripts.pdf2txt import extract_text
import os

from utils.dateu import get_current_time

directory_pdf=r'D:\zht\database\zoteroDB\storage'
directory_txt=r'D:\zht\database\projects\financial_paper_corpus'

def pdf2txt_0(path):
    name=os.path.basename(path)[:-4]
    extract_text([path],outfile=os.path.join(directory_txt,name+'.txt'))
    print(get_current_time(),name)

def task(path):
    try:
        pdf2txt_0(path)
    except:
        pass

def run():
    x = [os.path.join(r, file) for r, d, f in os.walk(directory_pdf) for file in
         f]
    paths = [f for f in x if f.endswith('.pdf')]
    parsed = os.listdir(directory_txt)
    paths = [p for p in paths if
             os.path.basename(p)[:-4] not in [a[:-4] for a in parsed]]
    pool = multiprocessing.Pool(6)
    pool.map(task, paths)


if __name__ == '__main__':
    run()











