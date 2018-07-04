# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-02  20:55
# NAME:zht-base_on_zotfile.py
import os
import sqlite3
import xmind
from dateutil.parser import parse
from datetime import timedelta


def get_pdf_and_notes(s):
    conn = sqlite3.connect(r'e:\a\zotero.sqlite')
    c = conn.cursor()

    def _query(q):
        c.execute(q)
        return c.fetchall()

    q1="select itemID from items where key = '%s'"%s
    itemID=_query(q1)[0][0]
    q2='select parentItemID from itemAttachments where itemID = "%s"'%itemID
    parentItemID=_query(q2)[0][0]
    q3='select note,title from itemNotes where parentItemID = "%s"'%parentItemID
    notes=_query(q3)
    q4='select path from itemAttachments where parentItemID = "%s"'%parentItemID
    pdf=_query(q4)[0][0][8:]
    c.close()
    return pdf,notes

def build_xmind(notes,pdf,xmindName):
    notes_hl=[n for n in notes if n[1]=='highlight']
    notes_ud=[n for n in notes if n[1]=='underline']

    w=xmind.load('123.xmind')
    s=w.getPrimarySheet()
    s.setTitle(xmindName)
    r=s.getRootTopic()
    r.setTitle(xmindName)
    t=r.addSubTopic()
    t.setTitle(pdf)
    if len(notes_hl)>0:
        hl=t.addSubTopic()
        hl.setTitle('highlight')
        for (text,type,link) in notes_hl:
            subt=hl.addSubTopic()
            subt.setTitle(text)
            subt.setURLHyperlink(link)

    if len(notes_ud) > 0:
        ud = t.addSubTopic()
        ud.setTitle('underline')
        for (text, type,link) in notes_ud:
            subt = ud.addSubTopic()
            subt.setTitle(text)
            subt.setURLHyperlink(link)
    xmind.save(w,os.path.join(r'e:\a',xmindName+'.xmind'))

def parse_date(title):
    ts=title.split(' (')[1].split(' ')[0] +' '+ title.split(' ')[-1][2:-1]
    tts= parse(ts)
    isPM=title.split(' ')[-1][:2]=='下午'
    if isPM:
        tts+=timedelta(hours=12)
    return tts

def run(iid):
    pdf,rawNotes=get_pdf_and_notes(iid)

    #get the latest extracted note
    ext_rawNotes=[]
    for rn,t in rawNotes:
        if t.startswith('Extracted Annotations'):
            ext_rawNotes.append((rn,parse_date(t)))
    note=sorted(ext_rawNotes,key=lambda x:x[1])[-1][0]
    lines=note.split('\n')

    notes=[]
    for l in lines[1:]:
        text=l.split(' (<a href="')[0][4:-1]
        type='highlight'
        if text.startswith('<u>'):
            text=text[3:-4]
            type='underline'
        link=l.split('href="')[-1].split('">')[0]
        #purify the text
        text=text.lstrip(',.? ')
        notes.append((text,type,link))

    build_xmind(notes, pdf, iid)


iid=r'68Y48YIT'
run(iid)

