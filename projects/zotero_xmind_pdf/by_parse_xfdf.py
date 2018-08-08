# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-08-06  20:08
# NAME:zht-by_parse_xfdf.py

import os
import re

import xmind
import argparse
from PyPDF2 import PdfFileReader
from PyPDF2.pdf import Destination
from mekk.xmind.document import SHAPE_RECTANGLE,SHAPE_UNDERLINE
from zht.projects.zotero_xmind_pdf.mekk_zht import XMindDocument

DIR_ROOT= r'D:\zht\database\zoteroDB\storage'
DIR_XMIND= r'D:\zht\database\xmind\research\xed'
DIR_XFDF=r'D:\zht\database\xfdf'

BLACK='#000000'
BLUE='#2d00f9'
GREEN='#6BE05F'
WHITE='#FFFFFF'

TITLE_COLOR=WHITE



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
        'phrase': [SHAPE_UNDERLINE, None, '#ff0000'],
        'sentence': [SHAPE_UNDERLINE, None, '#8A2BE2'],
        'ideas': [SHAPE_UNDERLINE, None, '#2d00f9']
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
            if color == TITLE_COLOR:
                return 'title'
            else:
                return 'sentence'
        else:
            raise ValueError

class Summary:
    def __init__(self,iid):
        self.iid=iid
        self.xfdf_path,self.pdf_name=self._get_path_and_name()
        self.run()

    def _get_path_and_name(self):
        dir_item = os.path.join(DIR_ROOT, self.iid)
        try:  # xfdf appears in the directory of zotero item
            fn = [n for n in os.listdir(dir_item) if n.endswith('.xfdf')][0]
            name = fn[:-5]
            xfdf_path = os.path.join(dir_item, fn)
        except:  # xfdf appears in DIR_XFDF
            fn_pdfs = [n for n in os.listdir(dir_item) if n.endswith('.pdf')]
            if len(
                    fn_pdfs) == 0:  # only one pdf appears in the directory of zotero item
                fn = fn_pdfs[0]
                name = fn[:-4]
            else:
                name = None
                for fn_pdf in fn_pdfs:
                    '''multiple pdfs appear in the directory of zotero item, 
                    we need to match them with the .xfdf files in DIR_XFDF to find
                    the target.'''
                    _nm = fn_pdf[:-4]
                    if _nm in [n[:-5] for n in os.listdir(DIR_XFDF)]:
                        name = _nm
                        break
            xfdf_path = os.path.join(DIR_XFDF, name + '.xfdf')
        return xfdf_path,name

    def parse_xfdf(self):
        '''
        refer to the standards of xfdf
        :return:
        '''
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(open(self.xfdf_path, encoding='utf8').read(), 'lxml')
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
                    text = contents.text.replace('\x8e ', 'fi').replace('\r\n',
                                                                        ' ').replace(
                        '\n', ' ').strip()
                    # text=ann.text.replace('\x8e ','fi').replace('\r\n',' ').replace('\n',' ').strip()
                    if len(text) > 0:
                        notes.append(
                            (Note(left=left,right=right,top=top,bottom=bottom, page=page,
                                  annotation_type=_type, text=text,
                                  color=color)))
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
                    t2.set_link(
                        'zotero://open-pdf/library/items/{}?page={}'.format(
                            self.iid,
                            note.page))
                    style = Summary.create_topic_style(xm, s)
                    t2.set_style(style)

                # for note in notes:
                #     if note.content_type == s:
                #         t2 = t1.add_subtopic(note.text)
                #         t2.set_link(
                #             'zotero://open-pdf/library/items/{}?page={}'.format(
                #                 self.iid,
                #                 note.page))
                #         style = Summary.create_topic_style(xm, s)
                #         t2.set_style(style)

        xm.save(xpath)
        os.startfile(xpath, 'open')

    def run(self):
        notes=self.parse_xfdf()
        # try:
        #     notes=self._identify_note_position(notes)
        # except:
        #     pass

        notes=self._identify_note_position(notes)
        # notes = sorted(notes, key=lambda x: (x.page, x.position, -x.bottom,x.left,-x.top,x.right))
        notes = sorted(notes, key=lambda x: (x.page, x.position,-x.top,x.right, -x.bottom,x.left))

        self.create_xmind_stacked(notes)


def debug():
    iid='T8Z36B47'
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
