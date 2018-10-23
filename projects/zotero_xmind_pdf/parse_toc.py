# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-10-20  08:52
# NAME:zht-parse_toc.py
import os
import shutil
from xml.etree import ElementTree as ET
import string
import pandas as pd
from PyPDF2 import PdfFileWriter,PdfFileReader
import subprocess
from bs4 import BeautifulSoup


class AddBookmarks:
    def __init__(self,pdf_path,method='bs'):
        self.pdf_path=pdf_path
        self.method=method
        self.df=self.parse_pdf()
        self.add_bookmarks()

    def get_root(self):
        xml_path=self.pdf_path[:-4]+'.xml'
        subprocess.call(['python', r'D:\app\python36\Scripts\pdf2txt.py', '-o', xml_path, self.pdf_path])
        with open(xml_path,'r',encoding='utf8') as f:
            s=f.read()
        tree=ET.fromstring(s)
        # tree=ET.parse(xml_path)
        root=tree.getroot()
        os.remove(xml_path)
        return root

    @staticmethod
    def detect_line_size(textline):
        size_l = []
        for _text in textline:
            if _text.text in string.ascii_letters:
                size_l.append(float(_text.attrib['size']))
        if len(size_l) > 0:
            return sum(size_l) / len(size_l)
        else:
            return 0

    @staticmethod
    def is_bold_line(textline, thresh=0.5):
        count_bold = 0
        total = 0

        for _text in textline:
            if 'font' in _text.attrib:
                if 'bold' in _text.attrib['font'].lower():
                    count_bold += 1
            total += 1
        if count_bold / total > thresh:
            return True
        else:
            return False

    def by_etree(self):
        root=self.get_root()
        items = []
        for page in root:
            page_id = int(page.attrib['id'])  # start from 1
            for textbox in page:
                if textbox.tag == 'textbox':
                    line_id = int(textbox.attrib['id'])  # start from 0
                    textline = textbox.find('textline')
                    line_content = ''.join([t.text for t in textline]).strip()
                    line_size = self.detect_line_size(textline)
                    is_bold = self.is_bold_line(textline)
                    items.append((page_id, line_id, is_bold, line_size, line_content))

        df = pd.DataFrame(items, columns=['page_id', 'line_id', 'is_bold', 'line_size', 'line_content'])
        return df

    def _merge_lines(self,df):
        # merge the lines sharing the same horizon
        df['line_spread_backward'] = df['top'] - df['top'].shift(1)
        df['line_spread_forward'] = df['top'] - df['top'].shift(-1)

        cols = [col for col in df.columns if col != 'line_content'] + ['line_content']
        df = df[cols]

        newdf = pd.DataFrame(columns=df.columns)
        newdf = newdf.append(df.iloc[0, :])

        for i in range(1, df.shape[0]):
            current_row = df.iloc[i, :]
            if current_row['line_spread_backward'] == 0:
                newdf.at[newdf.index[-1], 'line_content'] = ' '.join([newdf.at[newdf.index[-1], 'line_content'], current_row['line_content']])
                newdf.at[newdf.index[-1], 'right'] = current_row['right']
                newdf.at[newdf.index[-1], 'line_spread_forward'] = current_row['line_spread_forward']
            else:
                newdf = newdf.append(current_row)

        # trick: the value is rounded to three decimal places.
        newdf['line_spread'] = newdf[['line_spread_backward', 'line_spread_forward']].abs().min(axis=1).round(3)
        return newdf

    def _identify_title_lines(self,df):
        '''
        Several methods to identify titles:
        1. font
        2. line_spread
        3. prefix
        4. length (5 to 70)

        font seems to be the most powerful tool to find titles

        The main noise comes from the table and formula in the text.
        '''
        # TODO: the first page is exceptional

        # bk=df.copy()

        # narrow the scope down
        body_spread = df['line_spread'].value_counts().index[0]
        df['score_size'] = df['line_spread'].map(lambda x: 0 if x == body_spread else 1)

        df['len'] = df['line_content'].map(lambda s: len(s.replace(' ', '')))
        df['score_len'] = df['len'].map(lambda x: 1 if 5 <= x <= 100 else 0)

        prefixes = ('Abstract', 'I', 'V', 'X', 'Appendix', 'Introduction', 'Table', 'Fig',
                    '1', '2', '3', '4', '5', '6', '7', '8', '9')
        #TODO: How about A,B,C,D ? some papers use characters to list paragraphs

        df['score_prefix'] = df['line_content'].map(lambda x: 1 if x.startswith(prefixes) else 0)

        body_font = df['font'].value_counts().index[0]
        df['score_font'] = df['font'].map(lambda x: 0 if x == body_font else 1)

        df['score_bold']=df['font'].map(lambda x:1 if 'bold' in x.lower() else 0)
        #TODO: first page


        leftmost=df['left'].min()
        df['score_left']=df['left'].map(lambda x:1 if x<=leftmost+1 else 0) # add 1, since the setype may be not so precise
        #fixme: for paper with two columns (such as those from JFE) this method is highly biased.

        # fitler out lines with size being equal to 0
        df['score_linesize']=df['line_size'].map(lambda x:-100 if x==0 else 0)

        df['score'] = df[[col for col in df.columns if col.startswith('score')]].sum(axis=1)

        # target_font = df[df['score'] == df['score'].max()]['font'].value_counts().index[0]
        # df['is_title']=df.apply(
        #     lambda s:True if s['score']==df['score'].max() and
        #                      s['font']==target_font else False,axis=1)

        df['is_title']=df['score'].map(lambda x:True if x==df['score'].max() else False)

        # df['is_title'] = df['font'].map(lambda x: True if x == target_font else False)

        # df=df.sort_values('is_title',ascending=False)

        # df['font'].value_counts()
        #
        #
        # df=df.sort_values('score',ascending=False)
        #
        # a=df['left'].value_counts().sort_index()


        return df

    def by_bs(self):
        THRESH = 0.5
        xml_path=self.pdf_path[:-4]+'.xml'
        if not os.path.exists(xml_path):
            subprocess.call(['python', r'D:\app\python36\Scripts\pdf2txt.py', '-o', xml_path, self.pdf_path])

        with open(xml_path, 'r', encoding='utf8') as f:
            s = f.read()

        #delete xml file
        # os.remove(xml_path)

        soup = BeautifulSoup(s, 'xml')
        pages = soup.find_all('page')

        items = []
        for page in pages:
            page_id = int(page['id'])  # trick: starts from 1
            textboxs = page.find_all('textbox')

            line_id=0
            for textbox in textboxs:# textbox represents a paragraph
                # textline represents a row
                textlines=textbox.find_all('textline')
                for textline in textlines:
                    line_content = textline.text.replace('\n', '')
                    #left,bottom,right,top
                    l,b,r,t=(float(i) for i in textline['bbox'].split(','))
                    if len(line_content.replace(' ', '')) > 0:
                        # we do not use textbox id, since each textbox may contains multiple lines
                        line_id+=1

                        texts = list(textline.find_all('text'))

                        # identify font
                        fonts=[t['font'] for t in texts if 'font' in t.attrs]
                        font=max(set(fonts),key=fonts.count)

                        # identify size of each line
                        with_size=[t for t in texts if 'size' in t.attrs]
                        line_size = 0
                        if len(with_size) > 0:
                            line_size = sum(float(t['size']) for t in with_size) / len(with_size)

                        items.append((page_id, line_id, l,r,b,t,font, line_size, line_content))

        df = pd.DataFrame(items, columns=['page_id', 'line_id','left','right','bottom','top','font', 'line_size', 'line_content'])
        df=df.sort_values(['page_id','line_id'])
        df=self._merge_lines(df)
        df=self._identify_title_lines(df)
        return df

    def parse_pdf(self):
        if self.method=='bs':
            df=self.by_bs()
        else:
            df=self.by_etree()
        return df

    def add_bookmarks(self):
        title_df = self.df[self.df['is_title']] #trick: use font to identify the titles

        pdfReader = PdfFileReader(self.pdf_path)
        if pdfReader.isEncrypted:
            # TODO: decrypt error   refer to https://stackoverflow.com/questions/26242952/pypdf-2-decrypt-not-working
            #-------------------
            # pdfReader._override_encryption=True
            # pdfReader._flatten()
            #----------------------
            # pdfReader.decrypt('')
            #TODO: decrypt
            print(f'Encrypted file:\n\t\t {self.pdf_path}')
            pass
        else:
            pdfWriter = PdfFileWriter()
            for page in range(pdfReader.numPages):
                page_obj = pdfReader.getPage(page)
                pdfWriter.addPage(page_obj)

            for _, row in title_df.iterrows():
                pdfWriter.addBookmark(row['line_content'], row['page_id'] - 1)  # trick: the pagenum in pyPdf2 starts with 0

            with open(self.pdf_path, 'wb') as f:
                pdfWriter.write(f)

def identify_based_on_textbox():
    import pandas as pd
    from bs4 import BeautifulSoup

    path = r'E:\a\test_pdfminer\Westerlund et al- 2015- Testing for stock return predictability in a large Chinese panel.xml'

    with open(path, encoding='utf8') as f:
        soup = BeautifulSoup(f.read(), 'xml')

    pages = soup.find_all('page')

    items = []
    for page in pages:
        page_id = int(page['id'])
        textboxs = page.find_all('textbox')

        for textbox in textboxs:
            textbox_id = int(textbox['id'])
            left, bottom, right, top = (float(x) for x in textbox['bbox'].split(','))
            box_content = textbox.text.replace('\n', '')

            textlines = textbox.find_all('textline')
            if len(textlines) > 0:
                texts = textlines[0].find_all('text')
                fonts = [t['font'] for t in texts if 'font' in t.attrs]
                font = max(set(fonts), key=fonts.count)

                num_textline = len(textbox.find_all('textline'))

                items.append((page_id, textbox_id, num_textline, font, left, right, bottom, top, box_content))

    df = pd.DataFrame(items, columns=['page_id', 'textbox_id', 'num_textline', 'font', 'left', 'right', 'bottom', 'top', 'box_content'])

    df['top-bottom'] = df['top'] - df['bottom']

    test = df[df['num_textline'] == 1]

    test = test.sort_values('font')

    test = test.sort_values('top-bottom')
    test = test.sort_values('left')

    df['box_spread_backward'] = df['top'] - df['bottom'].shift(1)
    df['box_spread_forward'] = df['bottom'] - df['top'].shift(-1)

    df['box_spread'] = df[['box_spread_backward', 'box_spread_forward']].abs().min(axis=1)

    test = df[df['num_textline'] == 1]
    test = test.sort_values('box_spread')
    df = df.sort_values('box_spread')
    #TODO:



def debug():
    directory=r'E:\a\test_pdfminer'
    fn="Cheema and Nartea- 2017- Momentum returns, market states, and market dynamics - Is China different.pdf"
    path=os.path.join(directory,fn)
    AddBookmarks(path)

DEBUG=0


def task(path):
    AddBookmarks(path)

if __name__ == '__main__':
    if DEBUG:
        debug()
    else:
        directory=r'E:\a\test_pdfminer'
        fns=os.listdir(directory)
        fns=[fn for fn in fns if fn.endswith('.pdf')]

        paths=[]
        for fn in fns:
            path=os.path.join(directory,fn)
            paths.append(path)

        from zht.tools import multi_process

        multi_process(task,paths,n=6)




#TODO: if there is any bookmarks, skip the item
#TODO: multi_process

