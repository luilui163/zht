# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-01  22:27
# NAME:zht-base_on_foxit.py
import os
import sqlite3
import time
from collections import defaultdict
import re

import xmind
from dateutil.parser import parse
from datetime import timedelta
import argparse

ROOTDIR = r'D:\zht\database\zoteroDB\storage'
XMINDDIR = r'D:\zht\database\xmind\research\xed'

TYPE_MAP = {
    'Highlight': 'content',
    'Squiggly': 'relevant literature',
    'Underline': 'phrase',
    'StrikeOut': 'sentence',
    'Typewriter': 'ideas'
}

TYPE_ORDER = ['Typewriter', 'Highlight', 'Underline', 'Squiggly', 'StrikeOut']


def _setup_page_id_to_num(pdf, pages=None, _result=None, _num_pages=None):
    if _result is None:
        _result = {}
    if pages is None:
        _num_pages = []
        pages = pdf.trailer["/Root"].getObject()["/Pages"].getObject()
    t = pages["/Type"]
    if t == "/Pages":
        for page in pages["/Kids"]:
            _result[page.idnum] = len(_num_pages)
            _setup_page_id_to_num(pdf, page.getObject(), _result, _num_pages)
    elif t == "/Page":
        _num_pages.append(1)
    return _result

def recurse_tree(outlines, pg_id_num_map, parent):
    if isinstance(outlines, Destination):
        node = parent.addSubTopic()
        node.setTitle(outlines['/Title'])
        node.setURLHyperlink(str(pg_id_num_map[outlines.page.idnum] + 1))
        print(outlines['/Title'])
    else:
        for ol in outlines:
            recurse_tree(ol, pg_id_num_map, parent)


def create_xmind(iid, name, notes, outlines):
    '''

    :param name:name of the pdf or .fdf, does not contain suffix
    :param notes: list, each element containts a list,[type,content,page]
    [y,x,page,type,text]
    :return:
    '''
    directory = os.path.join(ROOTDIR, iid)

    w = xmind.load('123.xmind')
    s = w.getPrimarySheet()
    s.setTitle(name)
    r = s.getRootTopic()
    r.setTitle('annotations')
    t = r.addSubTopic()
    t.setTitle(name + '.pdf')
    # t.setURLHyperlink(os.path.join(directory,name+'.pdf'))
    t.setURLHyperlink('zotero://open-pdf/library/items/{}'.format(iid))

    for type in TYPE_ORDER:
        sub = t.addSubTopic()
        sub.setTitle(TYPE_MAP[type])
        for (y, x, page, type, text) in [n for n in notes if n[3] == type]:
            sub_ = sub.addSubTopic()
            sub_.setTitle(text)
            link = 'zotero://open-pdf/library/items/{}?page={}'.format(iid,
                                                                       page)  # trick:open pdf by zotero
            sub_.setURLHyperlink(link)

    xpath = os.path.join(XMINDDIR, name + '.xmind')
    xmind.save(w, xpath)
    # open the file
    os.startfile(xpath, 'open')


def clean_text(text):
    text = text.replace(r'\r\n', ' ').strip()
    # text=text.replace('&#x0D;&#x0A',' ')
    text = text.replace('\\', '')
    text = text.lstrip(r',.?')
    text = text.rstrip('(,')
    return text


def parse_fdf(iid):
    '''
    :param iid: str, like '68Y48YIT'
    :return: (list,str), the list contains a bunch of [y,x,page,type,text]
    '''
    directory = os.path.join(ROOTDIR, iid)
    fn = [n for n in os.listdir(directory) if n.endswith('.fdf')][0]
    name = fn[:-4]
    # with open(os.path.join(directory,fn),encoding='utf8',errors='ignore') as f:
    #     fdf=f.readlines()

    with open(os.path.join(directory, fn), encoding='iso-8859-15') as f:
        lines = f.readlines()

    validLines = []
    for type in TYPE_ORDER:
        for l in lines:
            if type in l:
                validLines.append(l)

    items = []
    for l in validLines:
        if 'Typewriter' in l:
            # .*? no greedy
            p = r'Rect\[ [0-9]*\.?[0-9]* ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*).*/Page (\d+).*/Contents\((.*?)\)'
            y, x, page, text = re.findall(p, l)[0]
            text = text.rstrip(r'\r')
            type = 'Typewriter'
        else:
            p = r'Rect\[ [0-9]*\.?[0-9]* ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*).*/Page (\d+).*/Subtype/(.*)/Type.*/Contents\((.*)\)/CA'
            y, x, page, type, text = re.findall(p, l)[0]
        # addjust page
        items.append(
            (float(y), float(x), int(page) + 1, type, clean_text(text)))

    # sort by page,y,x, y denote the height in the page
    items = sorted(items, key=lambda x: (x[2], -x[0], x[1]))
    return items, name


def run(iid):
    notes, name = parse_fdf(iid)
    create_xmind(iid, name, notes)


def debug():
    iid = 'KR7D86DV'
    run(iid)


from PyPDF2 import PdfFileReader
from PyPDF2.pdf import Destination

reader = PdfFileReader(
    r'D:\zht\database\zoteroDB\storage\KR7D86DV\Han et al- 2016- Taming Momentum Crashes - A Simple Stop-Loss Strategy.pdf')

w = xmind.load('123.xmind')
s = w.getPrimarySheet()
s.setTitle('toc')
r = s.getRootTopic()
r.setTitle('toc')

pdf_name = 'D:\zht\database\zoteroDB\storage\KR7D86DV\Han et al- 2016- Taming Momentum Crashes - A Simple Stop-Loss Strategy.pdf'
f = open(pdf_name, 'rb')
pdf = PdfFileReader(f)
pg_id_num_map = _setup_page_id_to_num(reader)
outlines = pdf.getOutlines()
recurse_tree(outlines, pg_id_num_map, r)

xpath = r'e:\a\xpath.xmind'
xmind.save(w, xpath)

DEBUG = 0

# if __name__ == '__main__':
#     if DEBUG:
#         debug()
#     else:
#         parser=argparse.ArgumentParser()
#         parser.add_argument('iid',metavar='i',type=str,help='an str for the zotero item')
#         args=parser.parse_args()
#         run(args.iid)


# TODO: save xmind in a given directory
# TODO:test with different pdf editer to check what's kind markup are supported in zotfile
# TODO: check what notes can be identified by zotfile
# TODO: open xmind automatically
# TODO: links between papers





