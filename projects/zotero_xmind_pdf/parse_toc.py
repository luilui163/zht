# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-06  11:15
# NAME:zht-parse_toc.py

import os
import sqlite3
import time
from collections import defaultdict
import re

import xmind
from dateutil.parser import parse
from datetime import timedelta
import argparse
from PyPDF2 import PdfFileReader
from PyPDF2.pdf import Destination
from mekk.xmind.document import TopicStyle, SHAPE_RECTANGLE, SHAPE_ELLIPSIS, \
    SHAPE_UNDERLINE
from mekk.xmind import XMindDocument


ROOTDIR=r'D:\zht\database\zoteroDB\storage'
XMINDDIR=r'D:\zht\database\xmind\research\xed'

TYPE_MAP={
    'Highlight':'content',
    'Squiggly':'relevant literature',
    'Underline':'phrase',
    'StrikeOut':'sentence',
    'Typewriter':'ideas'
}

STYLE={
    'Bookmark':[SHAPE_RECTANGLE,'#c6c6c6','#00000'],#[shape,fill_color,font_color]
    'Highlight':[SHAPE_UNDERLINE,'#F3F4F9','#00000'], # #F3F4F9 is the default color of the default theme
    'Squiggly':[SHAPE_UNDERLINE,'#F3F4F9','#0aff01'],
    'Underline':[SHAPE_UNDERLINE,'#F3F4F9','#ff0000'],
    'StrikeOut':[SHAPE_UNDERLINE,'#F3F4F9','#00ff2a'],
    'Typewriter':[SHAPE_UNDERLINE,'#F3F4F9','#2d00f9']
}

TYPE_ORDER=['Typewriter','Highlight', 'Underline', 'Squiggly', 'StrikeOut']


class Note:
    def __init__(self,ux,uy,page,type,text):
        self.ux=ux
        self.uy=uy
        self.type=type
        self.page=page
        self.text=text

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

def parse_toc(iid):
    fp = get_filepath(iid)
    pdf = PdfFileReader(open(fp, 'rb'))
    pg_id_num_map = _setup_page_id_to_num(pdf)
    toc = pdf.getOutlines()
    return toc,pg_id_num_map

def build_toc(iid,outlines, pg_id_num_map, parent):
    if isinstance(outlines,Destination):
        node=parent.addSubTopic()
        node.setTitle(outlines['/Title'])
        page=pg_id_num_map[outlines.page.idnum]+1
        link = 'zotero://open-pdf/library/items/{}?page={}'.format(iid, page)
        node.setURLHyperlink(link)
    else:
        for ol in outlines:
            build_toc(iid,ol, pg_id_num_map, parent)

def get_filepath(iid):
    fns=os.listdir(os.path.join(ROOTDIR,iid))
    paperName=[fn for fn in fns if fn.endswith('.pdf')][0]
    return os.path.join(ROOTDIR,iid,paperName)

def create_xmind(iid,name,notes,buildTOC=True):
    '''
    :param name:name of the pdf or .fdf, does not contain suffix
    :param notes: list, each element containts a list,[type,content,page]
    [y,x,page,type,text]
    :return:
    '''
    w=xmind.load('123.xmind')
    s=w.getPrimarySheet()
    s.setTitle(name)
    r=s.getRootTopic()
    r.setTitle('annotations')
    t=r.addSubTopic()
    t.setTitle(name+'.pdf')
    # t.setURLHyperlink(os.path.join(directory,name+'.pdf'))
    t.setURLHyperlink('zotero://open-pdf/library/items/{}'.format(iid))

    if buildTOC:
        node_toc= t.addSubTopic()
        node_toc.setTitle('TOC')
        toc,pg_id_num_map=parse_toc(iid)
        build_toc(iid,toc,pg_id_num_map,node_toc)

    notes=sorted(notes,key=lambda x:(x.page,x.uy,x.ux))
    types=[t for t in TYPE_ORDER if t in [n.type for n in notes]]
    for type in types:
        sub=t.addSubTopic()
        sub.setTitle(TYPE_MAP[type])
        for node in [n for n in notes if n.type==type]:
            sub_=sub.addSubTopic()
            sub_.setTitle(node.text)
            link='zotero://open-pdf/library/items/{}?page={}'.format(iid,node.page)#trick:open pdf by zotero
            sub_.setURLHyperlink(link)

    xpath=os.path.join(XMINDDIR,name+'.xmind')
    xmind.save(w,xpath)
    #open the file
    os.startfile(xpath,'open')

def clean_text(text):
    text=text.replace(r'\r\n',' ').strip()
    # text=text.replace('&#x0D;&#x0A',' ')
    text = text.replace('\\', '')
    text = text.lstrip(r',.?')
    text = text.rstrip('(,')
    return text

def parse_fdf(iid):
    '''
    :param iid: str, like '68Y48YIT'
    :return: (list,str), the list contains a bunch of [lx,ly,ux,uy,page,type,text]
    '''
    directory=os.path.join(ROOTDIR,iid)
    fn=[n for n in os.listdir(directory) if n.endswith('.fdf')][0]
    name=fn[:-4]
    with open(os.path.join(directory,fn),encoding='utf8',errors='ignore') as f:
        lines=f.readlines()

    lines=[l for l in lines if 'Contents' in l]

    # with open(os.path.join(directory,fn),encoding='iso-8859-15') as f:
    #     lines=f.readlines()

    validLines=[]
    for type in TYPE_ORDER:
        for l in lines:
            if type in l:
                validLines.append(l)

    notes=[]
    for l in validLines:
        if 'Typewriter' in l:
            # .*? no greedy
            p=r'Rect\[ ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*)\].*/Page (\d+).*/Contents\((.*?)\)'
            lx, ly, ux, uy,page,text=re.findall(p,l)[0]
            text=text.rstrip(r'\r')
            type='Typewriter'
        else:
            p=r'Rect\[ ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*)\].*/Page (\d+).*/Subtype/(.*)/Type.*/Contents\((.*)\)/CA'
            lx,ly,ux,uy,page,type,text=re.findall(p,l)[0]
        # addjust page
        notes.append(Note(float(ux),float(uy),int(page)+1,type,clean_text(text)))

    #sort by page,y,x, y denote the height in the page
    return notes,name

def get_notes_toc(iid):
    fp = get_filepath(iid)
    pdf = PdfFileReader(open(fp, 'rb'))
    pg_id_num_map = _setup_page_id_to_num(pdf)
    toc = pdf.getOutlines()

    f_toc = []

    def flatten_toc(toc):
        if isinstance(toc, Destination):
            return f_toc.append(toc)
        else:
            for t in toc:
                flatten_toc(t)

    flatten_toc(toc)
    notes_toc = []
    for t in f_toc:
        ux = 0
        uy = 10000
        page = pg_id_num_map[t.page.idnum] + 1
        type = 'Bookmark'
        text = t['/Title']
        notes_toc.append(Note(ux, uy, page, type, text))
    return notes_toc

def create_xmind_with_style(iid, name, notes):
    xpath=os.path.join(XMINDDIR,name+'.xmind')
    xm = XMindDocument.create('annotations', name)
    first_sheet = xm.get_first_sheet()
    root_topic = first_sheet.get_root_topic()
    for node in notes:
        t=root_topic.add_subtopic(node.text)
        t.set_link('zotero://open-pdf/library/items/{}?page={}'.format(iid, node.page))
        shape=STYLE[node.type][0]
        fill_color=STYLE[node.type][1]
        font_color=STYLE[node.type][2]
        style = XMindDocument.create_topic_style(xm,
                                                 shape=shape,
                                                 fill=fill_color,
                                                 line_color='#9400D3',
                                                 line_width='1pt',
                                                 font_color=font_color)
        t.set_style(style)

    xm.save(xpath)
    os.startfile(xpath, 'open')

def run(iid,mode=0):
    if mode==0:
        notes, name = parse_fdf(iid)
        notes_toc = get_notes_toc(iid)
        notes_comb = sorted(notes + notes_toc,
                            key=lambda x: (x.page, x.uy, x.ux))
        create_xmind_with_style(iid, name, notes_comb)
    else:
        notes, name = parse_fdf(iid)
        create_xmind(iid, name, notes)

def debug():
    iid='38Z9QERS'
    run(iid,mode=1)

debug()
