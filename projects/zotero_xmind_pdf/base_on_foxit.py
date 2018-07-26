# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-01  22:27
# NAME:zht-base_on_foxit.py

import os
import re

import xmind
import argparse
from PyPDF2 import PdfFileReader
from PyPDF2.pdf import Destination
from mekk.xmind.document import SHAPE_RECTANGLE,SHAPE_UNDERLINE
from zht.projects.zotero_xmind_pdf.mekk_zht import XMindDocument

ROOTDIR=r'D:\zht\database\zoteroDB\storage'
XMINDDIR=r'D:\zht\database\xmind\research\xed'

TYPE_MAP_fdf={
    'highlight':'content',
    'squiggly':'relevant literature',
    'underline':'phrase',
    'strikeout':'sentence',
    'typewriter':'ideas'
}
TYPE_MAP_xfdf={
    'highlight':'content',
    'squiggly':'relevant literature',
    'underline':'phrase',
    'strikeout':'sentence',
    'freetext':'ideas'
}


BLACK='#000000'
BLUE='#2d00f9'



STYLE={
    'title':[SHAPE_RECTANGLE,'#c6c6c6',BLACK],#[shape,fill_color,font_color]
    'highlight':[SHAPE_UNDERLINE,None,'#00000'], # #F3F4F9 is the default color of the default theme
    'squiggly':[SHAPE_UNDERLINE,None,'#0aff01'],
    'underline':[SHAPE_UNDERLINE,None,'#ff0000'],
    'strikeout':[SHAPE_UNDERLINE,None,'#8A2BE2'],
    'typewriter':[SHAPE_UNDERLINE,None,'#2d00f9'],
    'freetext':[SHAPE_UNDERLINE,None,'#2d00f9']
}

TYPE_ORDER=['typewriter','highlight', 'underline', 'squiggly', 'strikeout']


class Note:
    def __init__(self,lx,ly,ux,uy,page,type,text,position=-1,color=None):
        self.lx=lx
        self.ly=ly
        self.ux=ux
        self.uy=uy
        self.type=type
        self.page=page
        self.text=text
        self.position=position # which part of the annotation belongs, -1 denotes left,1 denotes right
        self.color=color

    def __eq__(self, other):
        return (self.type==other.type and self.text==other.text and self.color==other.color and self.page==other.page)

    def __hash__(self):
        return hash((self.type,self.text,self.color,self.page))

    def __lt__(self, other):
        raise NotImplementedError



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
        sub.setTitle(TYPE_MAP_fdf[type])
        for node in [n for n in notes if n.type==type]:
            sub_=sub.addSubTopic()
            sub_.setTitle(node.text)
            link='zotero://open-pdf/library/items/{}?page={}'.format(iid,node.page)#trick:open pdf by zotero
            sub_.setURLHyperlink(link)

    xpath=os.path.join(XMINDDIR,name+'.xmind')
    xmind.save(w,xpath)
    #open the file
    os.startfile(xpath,'open')

def valid_xml_char_ordinal(c):
    codepoint = ord(c)
    # conditions ordered by presumed frequency
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
        )

def clean_text(text):
    text=''.join(c for c in text if valid_xml_char_ordinal(c))
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
    #TODO: how to parse fdf contains Chinese character?
    # from encodings.aliases import aliases
    # ecs = list(set(aliases.values()))
    #
    # with open(r'e:\a\test.txt','w') as f:
    #     for ec in ecs:
    #         try:
    #             text=open(os.path.join(directory, fn), encoding=ec,errors='ignore').readlines()[270]
    #             f.write("{}---------------------->{}\n\n".format(ec,text))
    #         except:
    #             pass

    lines=[l for l in lines if 'Contents' in l]

    # with open(os.path.join(directory,fn),encoding='iso-8859-15') as f:
    #     lines=f.readlines()

    validLines=[]
    for type in TYPE_ORDER:
        for l in lines:
            if type in l.lower():
                validLines.append(l)

    notes=[]
    for l in validLines:
        if 'typewriter' in l.lower():
            # .*? no greedy
            p=r'Rect\[ ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*)\].*/Page (\d+).*/Contents\((.*?)\)'
            lx, ly, ux, uy,page,text=re.findall(p,l)[0]
            text=text.replace(r'\n',' ')
            text=text.replace(r'\r',' ')
            type='typewriter'
        else:
            p=r'Rect\[ ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*)\].*/Page (\d+).*/Subtype/(.*)/Type.*/Contents\((.*)\)/CA'
            lx,ly,ux,uy,page,type,text=re.findall(p,l)[0]
        # addjust page
        if len(text)>0:
            notes.append(Note(float(lx),float(ly),float(ux),float(uy),int(page)+1,type.lower(),clean_text(text)))

    #sort by page,y,x, y denote the height in the page
    return notes,name

def parse_xfdf(iid):
    directory=os.path.join(ROOTDIR,iid)
    fn=[n for n in os.listdir(directory) if n.endswith('.xfdf')][0]
    name=fn[:-5]
    from bs4 import BeautifulSoup
    soup=BeautifulSoup(open(os.path.join(directory,fn),encoding='utf8').read(),'lxml')
    # soup=BeautifulSoup(open(os.path.join(directory,fn),'rb').read(),'lxml')
    notes=[]
    for _type in TYPE_MAP_xfdf.keys():
        anns=soup.findAll(_type)
        for ann in anns:
            if ann.text:
                page=int(ann['page'])+1
                color=ann['color']
                lx, ly, ux, uy=(float(s) for s in ann['rect'].split(','))
                text=ann.p.text.replace('\x8e ','fi').replace('\r\n',' ').replace('\n',' ')
                if len(text)>0:
                    notes.append((Note(lx=lx,ly=ly,ux=ux,uy=uy,page=page,type=_type,text=text,color=color)))
    return notes,name


def get_notes_toc(iid):
    fp = get_filepath(iid)
    pdf = PdfFileReader(open(fp, 'rb'))
    if pdf.isEncrypted:
        '''
        https://stackoverflow.com/questions/26242952/pypdf-2-decrypt-not-working

        test with 6ZMKYDPP
        '''
        #TODO: parse the bookmark when the pdf is encrypted.
        print('PDF is encrypted, can not parse the bookmarks.')
        return []
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
        lx=0
        ly=10000
        ux = 0
        uy = 10000 # just set a random large number
        page = pg_id_num_map[t.page.idnum] + 1
        type ='title'
        text = t['/Title']
        notes_toc.append(Note(lx,ly,ux, uy, page, type, text))
    return notes_toc

def create_topic_style(xmd,type):
    shape = STYLE[type][0]
    fill_color = STYLE[type][1]
    font_color = STYLE[type][2]
    style = XMindDocument.create_topic_style(xmd,
                                             shape=shape,
                                             fill=fill_color,
                                             line_color='#9400D3',
                                             line_width='1pt',
                                             font_color=font_color,
                                             )
    return style

def create_xmind_with_style(iid, name, notes):
    xpath=os.path.join(XMINDDIR,name+'.xmind')
    xm = XMindDocument.create('annotations', iid)
    first_sheet = xm.get_first_sheet()
    root_topic = first_sheet.get_root_topic()
    first_topic=root_topic.add_subtopic(name+'.pdf')
    first_topic.set_link('zotero://open-pdf/library/items/{}'.format(iid))
    for note in notes:
        if note.type!='strikeout':
            t=first_topic.add_subtopic(note.text)
            t.set_link('zotero://open-pdf/library/items/{}?page={}'.format(iid, note.page))
            style=create_topic_style(xm,note.type)
            t.set_style(style)

    # create a subtopic for strikeout, and typewriter alone
    for s in ['typewriter','strikeout']:
        t1=first_topic.add_subtopic(TYPE_MAP_fdf[s])
        if s=='typewriter':
            t1.add_marker('flag-red')
        t1.set_style(create_topic_style(xm,s))
        for note in notes:
            if note.type==s:
                t2=t1.add_subtopic(note.text)
                t2.set_link('zotero://open-pdf/library/items/{}?page={}'.format(iid,
                                                                               note.page))
                style = create_topic_style(xm, note.type)
                t2.set_style(style)

    xm.save(xpath)
    os.startfile(xpath, 'open')

def create_xmind_stacked(iid,name,notes):
    xpath=os.path.join(XMINDDIR,name+'.xmind')
    xm = XMindDocument.create('annotations', iid)
    first_sheet = xm.get_first_sheet()
    root_topic = first_sheet.get_root_topic()
    first_topic=root_topic.add_subtopic(name+'.pdf')
    first_topic.set_link('zotero://open-pdf/library/items/{}'.format(iid))

    ns1=[note for note in notes if note.type not in ['strikeout']]
    last_title=first_topic
    for note in ns1:
        if note.type=='title':
            t=first_topic.add_subtopic(note.text)
            last_title=t
        else:
            t=last_title.add_subtopic(note.text)
        t.set_link(
            'zotero://open-pdf/library/items/{}?page={}'.format(iid, note.page))
        style = create_topic_style(xm, note.type)
        t.set_style(style)

    # create a subtopic for strikeout, and typewriter alone
    for s in ['typewriter','strikeout']:
        t1=first_topic.add_subtopic(TYPE_MAP_fdf[s])
        if s=='typewriter':
            t1.add_marker('flag-red')
        t1.set_style(create_topic_style(xm,s))
        for note in notes:
            if note.type==s:
                t2=t1.add_subtopic(note.text)
                t2.set_link('zotero://open-pdf/library/items/{}?page={}'.format(iid,
                                                                               note.page))
                style = create_topic_style(xm, note.type)
                t2.set_style(style)

    xm.save(xpath)
    os.startfile(xpath, 'open')


def identify_position(notes):
    '''
    identify the position of the notes, determine which part the notes appear,
    left or right

    :param notes:
    :return:
    '''
    min_left=99999
    max_right=0
    min_page=100000
    for note in notes:
        if note.type in ['highlight','squiggly','underline','strikeout']:
            if note.lx<min_left:
                min_left=note.lx
            if note.ux>max_right:
                max_right=note.ux
            if note.page<min_page:
                min_page=note.page

    thresh=0.5*(min_left+max_right)
    for note in notes:
        if note.type in ['highlight','squiggly','underline','strikeout']:
            if note.ux<thresh:
                note.position=-1 #-1 denote left, 1 denote right
            elif note.lx>thresh:
                note.position=1
            elif note.page==min_page:
                # trick: the notes in first annotation page may belong to abstract, but, usually, the abstract part won't be divided into left part and right part,so we just skip it
                pass
            else:
                raise ValueError('Can not identify the position of : \n\n"{}" \n{}'.format(note.type,note.text))
    return notes

def identify_title(notes):
    for note in notes:
        if note.type=='underline' and note.color=='#FFFFFF':
            note.type='title'
    return notes


def run(iid,column=1,mode=0,title_mode='annotation'):
    if mode==0:
        directory = os.path.join(ROOTDIR, iid)
        xfdfs=[n for n in os.listdir(directory) if n.endswith('.xfdf')]
        if len(xfdfs)>0:
            notes,name=parse_xfdf(iid)
        else:
            notes,name=parse_fdf(iid)

        notes=list(set(notes))#trick:handle duplicates

        if column==2:
            notes=identify_position(notes)
        if title_mode=='annotation':
            notes=identify_title(notes)
            notes=sorted(notes,key=lambda x:(x.page,x.position,-x.uy,x.ux))
            create_xmind_stacked(iid,name,notes)
            # create_xmind_with_style(iid,name,notes)
        else:
            notes_toc = get_notes_toc(iid)
            notes_comb = sorted(notes + notes_toc,
                                key=lambda x: (x.page,x.position,-x.uy, x.ux))
            create_xmind_with_style(iid, name, notes_comb)
    else:
        notes, name = parse_fdf(iid)
        create_xmind(iid, name, notes)

def debug():
    iid='3N4UJRP3'
    run(iid,column=2)



DEBUG=1

if __name__ == '__main__':
    if DEBUG:
        debug()
    else:
        parser=argparse.ArgumentParser()
        parser.add_argument('iid',metavar='i',type=str,help='an str for the zotero item')
        parser.add_argument('column',metavar='c',type=int,help='column number of the paper')
        args=parser.parse_args()
        run(args.iid,args.column)
#TODO: filter duplicates automatically
#TODO: why not use annotation to identify the titles, so we do not need to parse the bookmarks. In the other hand, we can identify the specific position of the title in the page.
#TODO: how to parse fdf contains Chinese character?   FBSPMJSM
#TODO: use adobe acrobat reader to export the comments as .xfdf, this format is more clear and easy to parse. But it seems only support a several annotation formats.
#TODO: Chinese characters can not be identified appropariate,refer to HXFA72N7
#TODO: read tags from zotero's sqlite and then add it to the .xmind
#TODO: can we develop tool to make .xmind to be interactive with pdf, that is, if we delete an annotation in .xmind, it will also be deleted in pdf,and once we add a new annotation in pdf, it will automatically update in .xmind just like docear
#TODO: how to set the font? "open Sans"
#TODO: automatically add a xed tag to paper
#TODO: extract the color of bookmarks, and customize style in xmind
#TODO: use mekk to customize style
#TODO: how to build the TOC tree
#TODO: save xmind in a given directory
#TODO:test with different pdf editer to check what's kind markup are supported in zotfile
#TODO: check what notes can be identified by zotfile
#TODO: open xmind automatically
#TODO: links between papers
#TODO: when the paper has two columns,take 'management science' for example, if
# we just sort on page,ux and uy, the result is a mess






