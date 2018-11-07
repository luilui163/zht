# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-08-06  20:08
# NAME:zht-annotation_to_xmind.py

import os
# import re
# from collections import OrderedDict

# import xmind
import argparse
# from PyPDF2 import PdfFileReader
# from PyPDF2.pdf import Destination
from mekk.xmind.document import SHAPE_RECTANGLE,SHAPE_UNDERLINE
from webcolors import rgb_to_hex
from zht.projects.zotero_xmind_pdf.mekk_zht import XMindDocument

DIR_ROOT= r'D:\zht\database\zoteroDB\storage'
DIR_XMIND= r'D:\zht\database\xmind\research\xed'
DIR_XFDF=r'D:\zht\database\xfdf'
DIR_FDF=r'D:\zht\database\fdf'

BLACK='#000000'
BLUE='#2d00f9'
GREEN='#6BE05F'
BUGN='#27AE60'
WHITE='#FFFFFF'
RED='#FE2600'


TITLE_COLOR=WHITE

def valid_xml_char_ordinal(c):
    codepoint = ord(c)
    # conditions ordered by presumed frequency
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
        )

class Note:
    TYPE_MAP_xfdf = {
        'highlight': 'content',
        'squiggly': 'literature',
        'underline': 'phrase',
        'strikeout': 'sentence',
        'freetext': 'ideas'
    }

    STYLE = {
        'title': [SHAPE_RECTANGLE, '#c6c6c6', BLACK],
        # [shape,fill_color,font_color]
        'content': [SHAPE_UNDERLINE, None, BLACK],
        # #F3F4F9 is the default color of the default theme
        'literature': [SHAPE_UNDERLINE, None, GREEN],
        'phrase': [SHAPE_UNDERLINE, None, BLUE],
        'sentence': [SHAPE_UNDERLINE, None, BUGN],
        'ideas': [SHAPE_UNDERLINE, None, RED]
    }

    def __init__(self, left,right,top,bottom, page, annotation_type, text, position=-1, color=None):
        self.left=left#left bottom
        self.right=right#left top
        self.top=top#right bottom
        self.bottom=bottom#right top
        self.height=self.top-self.bottom
        self.annotation_type=annotation_type
        self.page=page
        self.text=text
        self.position=position # which part of the annotation belongs, -1 denotes left,1 denotes right
        self.color=color
        self.content_type=self.identify_content_type(self.annotation_type, self.color)

    def __eq__(self, other):
        return (self.annotation_type == other.annotation_type and self.text == other.text and self.color == other.color and self.page == other.page)

    def __hash__(self):
        return hash((self.annotation_type, self.text, self.color, self.page))

    def __lt__(self, other):
        raise NotImplementedError

    def is_inside(self,other):
        return other.left<=self.left and other.right>=self.left and other.bottom>=self.bottom and other.top<=self.top

    @staticmethod
    def identify_content_type(anno_type, color):
        if anno_type == 'highlight':
            return 'content'
        elif anno_type == 'underline':
            return 'phrase'
        elif anno_type == 'squiggly':
            return 'literature'
        elif anno_type == 'freetext':
            return 'ideas'
        elif anno_type == 'strikeout':
            if color.upper() == TITLE_COLOR:
                return 'title'
            else:
                return 'sentence'
        else:
            return 'content'
            # raise ValueError

class Summary:
    def __init__(self,iid):
        self.iid=iid
        self.annot_path,self.pdf_name=self._get_path_and_name()
        self.run()

    def _get_path_and_name(self):
        dir_item = os.path.join(DIR_ROOT, self.iid)
        name=None
        annot_path=None
        xfdfs=[n for n in os.listdir(dir_item) if n.endswith('.xfdf')]
        fdfs=[n for n in os.listdir(dir_item) if n.endswith('.fdf')]
        if len(xfdfs)>0:#xfdf appears in the directory of zotero item
            name=xfdfs[0][:-5]
            annot_path=os.path.join(dir_item,xfdfs[0])
        elif len(fdfs)>0:
            name=fdfs[0][:-4]
            annot_path=os.path.join(dir_item,fdfs[0])
        else:# xfdf appears in DIR_XFDF
            fn_pdfs = [n for n in os.listdir(dir_item) if n.endswith('.pdf')]
            if len(fn_pdfs) ==1:  # only one pdf appears in the directory of zotero item
                fn = fn_pdfs[0]
                name = fn[:-4]
                p_xfdf=os.path.join(DIR_XFDF,name+'.xfdf')
                p_fdf=os.path.join(DIR_FDF,name+'.fdf')
                if os.path.exists(p_xfdf):
                    annot_path=p_xfdf
                elif os.path.exists(p_fdf):
                    annot_path=p_fdf
            else:
                for fn_pdf in fn_pdfs:
                    '''multiple pdfs appear in the directory of zotero item, 
                    we need to match them with the .xfdf files in DIR_XFDF to find
                    the target.'''
                    p_xfdf = os.path.join(DIR_XFDF, fn_pdf[:-4] + '.xfdf')
                    p_fdf = os.path.join(DIR_XFDF, fn_pdf[:-4] + '.xfdf')

                    if os.path.exists(p_xfdf):
                        name=fn_pdf[:-4]
                        annot_path=p_xfdf
                        break
                    elif os.path.exists(p_fdf):
                        name=fn_pdf[:-4]
                        annot_path=p_fdf
                        break
        return annot_path,name

    def parse_xfdf(self):
        '''
        refer to the standards of xfdf
        :return:
        '''
        from bs4 import BeautifulSoup
        with open(self.annot_path,encoding='utf8') as f:
            soup=BeautifulSoup(f.read(),'lxml')
        # soup = BeautifulSoup(open(self.xfdf_path, encoding='utf8').read(), 'lxml')
        # soup=BeautifulSoup(open(os.path.join(directory,fn),'rb').read(),'lxml')
        notes = []
        for _type in Note.TYPE_MAP_xfdf.keys():
            anns = soup.findAll(_type)
            for ann in anns:
                if ann.text:
                    page = int(ann['page']) + 1
                    color = ann['color'] if _type not in [
                        'freetext'] else None  # freetext does not contain color attribute
                    # lx, ly, ux, uy = (float(s) for s in ann['rect'].split(','))
                    left,bottom,right,top=(float(s) for s in ann['rect'].split(','))
                    # left_bottom,left_top,right_bottom,right_top = (float(s) for s in ann['rect'].split(','))

                    contents = ann.find('contents-richtext')
                    text = contents.text.replace('\x8e ', 'fi').replace('\r\n',' ').replace('\n', ' ').strip()
                    # text=ann.text.replace('\x8e ','fi').replace('\r\n',' ').replace('\n',' ').strip()
                    notes.append((Note(left=left,right=right,top=top,bottom=bottom, page=page,
                              annotation_type=_type, text=text,
                              color=color)))
        return notes

    def parse_fdf_from_adobe(self):
        def _filter_text(text):
            text=text.replace('\(','(').replace('\)',')')
            text=text.replace('\\r\\n',' ').strip()
            text=''.join(c for c in text if valid_xml_char_ordinal(c))#filter out invalid characteristics
            return text

        with open(self.annot_path,encoding='utf8',errors='ignore') as f:
            text=f.read()
        annots = text.split('0 obj\n')
        annots=[ann for ann in annots if ann.startswith('<</Border')]

        notes=[]
        for t in annots:
            color_list = t.split(']/CA')[0].split('[')[-1].split(' ')
            color = rgb_to_hex(list(int(round(float(c) * 255)) for c in color_list))
            text = '/Contents('.join(t.split('/Contents(')[1:]).split(')/CreationDate(')[0]
            text=_filter_text(text)
            rect = t.split('/Rect[')[-1].split(']')[0].split(' ')
            left, bottom, right, top = (float(r) for r in rect)
            _type = t.split('Subtype/')[-1].split('/')[0].lower()
            page = int(t.split('/Popup')[0].split('Page ')[-1])+1
            notes.append(Note(left=left,right=right,top=top,bottom=bottom, page=page,
                              annotation_type=_type, text=text,
                              color=color))
        return notes

    def parse_fdf_from_foxit(self):
        def _filter_text(text):
            str_map={
                '\(':'(',
                '\)':')',
                '\\\\':'"', #replace '\\' with '"'
                '\\x82':'fl',
                '\\x83':'fi',
                '\\x84':'—',
                '\\x85':'-',
                '\\x8a':'-',
                '\\x8d':'“',
                '\\x8e':'”',
                '\\x8f':"'",
                # '\\x8f\\x8f':'"',
                # '\\x8e':'"',
                '\\x90':"'",
                '\\xa4':'ff',
                '\\xa5':'¥',
                '\\xb1':'α',
                '\\xb2':'β',
                '\\xb3':'γ',
                '\\xb4':'δ',
                '\\xb5':'ε',
                '\\xbb':'λ',
                '\\xc1':'ρ',
                '\\xd7':'x',
                '\\xe1':'á',
                '\\xe4':'ä',
                '\\xef':'ï',
                '\\xf6':'ö',
                '\\xf8':'ø',
                '\\xfe':'+',
                # '\\xfe\\xff':'',
                '\\r\\n':' ',
                '\\r':' ',
                '  ':' ',
                '+\\xff':'',
                #http://mindprod.com/jgloss/ascii.html
            }

            text=''.join(c for c in text if valid_xml_char_ordinal(c))#filter out invalid characteristics
            for k in str_map.keys():
                text=text.replace(k,str_map[k])

            return text

        # with open(self.annot_path, encoding='utf8', errors='ignore') as f:
        #     lines = f.readlines()
        with open(self.annot_path, encoding='utf8', errors='backslashreplace') as f:
            lines = f.readlines()


        lines = [l for l in lines if 'Contents' in l]
        notes=[]
        for l in lines:
            if 'FreeTextTypewriter' in l:
                text=l.split('/Contents(')[-1].split(')/')[0]
                text=_filter_text(text)
                rect=l.split(']')[0].split('[ ')[1].split(' ')
                left, bottom, right, top = (float(r) for r in rect)
                _type='freetext'
                page=int(l.split('/AP')[0].split('/Page ')[-1])+1
                color=None
                notes.append(Note(left=left, right=right, top=top, bottom=bottom, page=page,
                                  annotation_type=_type, text=text,
                                  color=color))
            else:
                color_list = l.split(']')[0].split('[ ')[-1].split(' ')
                color = rgb_to_hex(list(int(round(float(c) * 255)) for c in color_list))
                text = l.split('Annot/Contents(')[-1].split(')/CA')[0]
                text = _filter_text(text)
                rect=''.join(l.split('Rect[ ')[1:]).split(']/')[0].split(' ')
                # rect = l.split(']/F')[0].split('Rect[ ')[-1].split(' ')
                left, bottom, right, top = (float(r) for r in rect)
                _type = l.split('Subtype/')[-1].split('/Type')[0].lower()
                page=int(l.split('/Page ')[1].split('/')[0])+1
                # page = int(l.split('/RC')[0].split('/Page ')[-1])+1
                notes.append(Note(left=left, right=right, top=top, bottom=bottom, page=page,
                                  annotation_type=_type, text=text,
                                  color=color))

        return notes

    @staticmethod
    def filter_notes(notes):
        ns = list(set(notes))  # trick:handle duplicates
        ns = [n for n in ns if len(n.text) > 2]  # delete those short notes
        return ns

    @staticmethod
    def detect_row_height(notes):
        min_spread = 100000
        for note in [n for n in notes if n.annotation_type=='highlight']:
            if note.height<min_spread:
                min_spread=note.height

        if min_spread==10000:
            raise ValueError('Can not detect row height')
        return min_spread

    @staticmethod
    def _identify_note_position(notes):
        '''
        identify the position of the notes, determine which part the notes appear,
        left or right
        '''
        min_left = 99999
        max_right = 0
        min_page = 100000
        for note in notes:
            if note.annotation_type in ['highlight', 'squiggly', 'underline', 'strikeout']:
                if note.left < min_left:
                    min_left = note.left
                if note.right > max_right:
                    max_right = note.right
                if note.page < min_page:
                    min_page = note.page

        middle = 0.5 * (min_left + max_right)
        success=0
        for note in notes:
            if note.annotation_type in ['highlight', 'squiggly', 'underline', 'strikeout']:
                if note.right < middle:
                    note.position = -1  # -1 denote left, 1 denote right
                    success+=1
                elif note.left > middle:
                    note.position = 1
                    success+=1
                elif note.page == min_page:
                    # trick: the notes in first annotation page may belong to abstract, but, usually, the abstract part won't be divided into left part and right part,so we just skip it
                    pass
                elif note.height>Summary.detect_row_height(notes):
                    pass
                else:
                    pass
                    # raise ValueError(
                    #     'Can not identify the position of : \n\n"{}" \n{}'.format(
                    #         note.content_type, note.text))

        if success/len(notes)<=0.8:#trick:if the seperated ratio is less than 0.8, it is not a two-columns paper, reset all the position to -1
            for n in notes:
                n.position=-1
        return notes

    @staticmethod
    def create_topic_style(xmd, type):
        shape = Note.STYLE[type][0]
        fill_color = Note.STYLE[type][1]
        font_color = Note.STYLE[type][2]
        style = XMindDocument.create_topic_style(xmd,
                                                 shape=shape,
                                                 fill=fill_color,
                                                 line_color='#9400D3',
                                                 line_width='1pt',
                                                 font_color=font_color,
                                                 )
        return style

    def create_xmind_stacked(self,notes):
        xpath = os.path.join(DIR_XMIND, self.pdf_name + '.xmind')
        xm = XMindDocument.create('annotations', self.iid)
        first_sheet = xm.get_first_sheet()
        root_topic = first_sheet.get_root_topic()
        first_topic = root_topic.add_subtopic(self.pdf_name + '.pdf')
        first_topic.set_link('zotero://open-pdf/library/items/{}'.format(self.iid))

        ns1 = [note for note in notes if note.content_type not in ['sentence']]
        last_title = first_topic
        for note in ns1:
            if note.content_type == 'title':
                t = first_topic.add_subtopic(note.text)
                last_title = t
            else:
                t = last_title.add_subtopic(note.text)
            t.set_link(
                'zotero://open-pdf/library/items/{}?page={}'.format(self.iid,
                                                                    note.page))
            style = Summary.create_topic_style(xm, note.content_type)
            t.set_style(style)

        # create a subtopic for strikeout, and freetext alone
        for s in ['ideas', 'sentence']:
            ns = [n for n in notes if n.content_type == s]
            if len(ns) > 0:
                t1 = first_topic.add_subtopic(s)
                if s=='ideas':
                    t1.add_marker('flag-red')
                t1.set_style(Summary.create_topic_style(xm, s))
                for note in ns:
                    t2 = t1.add_subtopic(note.text)
                    t2.set_link('zotero://open-pdf/library/items/{}?page={}'.format(self.iid,note.page))
                    style = Summary.create_topic_style(xm, s)
                    t2.set_style(style)

        xm.save(xpath)
        os.startfile(xpath, 'open')

    @staticmethod
    def clean_notes(notes):

        # 'a b s t r a c t'
        for n in notes:
            if n.text.replace(' ','').lower()=='abstract':
                n.text=n.text.replace(' ','')

        return [n for n in notes if len(n.text)>2]

    def run(self):
        if self.annot_path.endswith('.xfdf'):
            notes=self.parse_xfdf()
        else:
            with open(self.annot_path,encoding='utf8',errors='ignore') as f:
                lines=f.readlines()
            if lines[1].startswith('%'):
                notes=self.parse_fdf_from_adobe()
            else:
                notes=self.parse_fdf_from_foxit()
        # try:
        #     notes=self._identify_note_position(notes)
        # except:
        #     pass
        notes=self.clean_notes(notes)
        notes=self._identify_note_position(notes)
        # notes = sorted(notes, key=lambda x: (x.page, x.position, -x.bottom,x.left,-x.top,x.right))
        notes = sorted(notes, key=lambda x: (x.page, x.position,-x.top,x.right, -x.bottom,x.left))

        self.create_xmind_stacked(notes)

def debug():
    iid='7JHC6TZC'
    Summary(iid)

DEBUG=0

if __name__ == '__main__':
    if DEBUG:
        debug()
    else:
        parser=argparse.ArgumentParser()
        parser.add_argument('iid',metavar='i',type=str,help='an str for the zotero item')
        # parser.add_argument('column',metavar='c',type=int,help='column number of the paper')
        args=parser.parse_args()
        Summary(args.iid)

#TODO: combine notes splitted by pages
#TODO: read zotero.sqlite to find iid itself rather than input manually
#TODO: automatically output .xfdf with the help of 按键精灵
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
'''
1. store the unique id of every annotation from .fdf or .xfdf and generate id for 
reach xmind element based on the id from annotation. With the id mapped from 
annotation to xmind element, we can monitor the annotations in pdf and update
the new added annotation without changing the structure of the xmind. We can also
store the annotation time in the id of xmind element.  Similiar to the function 
in docear.



'''

