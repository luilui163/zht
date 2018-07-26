# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-22  22:48
# NAME:zht-split2.py



import zipfile

from bs4 import BeautifulSoup
from lxml import etree

fp=r'e:\a\toedit1.xmind'
archive=zipfile.ZipFile(fp,'r')

content=archive.open('content.xml').read()

soup=BeautifulSoup(content,'lxml')

import re




def is_paper_tag(tag):
    p1=re.compile('zotero://open-pdf/library/items/.*')
    p2=re.compile('.pdf')
    if tag.name=='topic':
        if tag.has_attr('xlink:href'):
            if p1.search(tag['xlink:href']) or p2.search(tag['xlink:href']):
                if 'page' not in tag['xlink:href']:
                    return True
    else:
        return False

papers=soup.find_all(is_paper_tag)

keep=0
paper=papers[keep]

iid=paper['xlink:href'].split('/')[-1]
#
# s=soup
# s.sheet.topic.title=iid
# s.sheet.topics.clear()
# s.sheet.topics.append(paper) #TODO: how about set the "children" tag in document as the "children" of paper directly?

for i in range(len(papers)):
    if i!=keep:
        papers[i].decompose()

test_papers=soup.find_all(is_paper_tag)


len(soup.text)


style_id0=paper['style-id']
style_ids=[st['style-id'] for st in paper.find_all(attrs={'style-id':True})]

style_ids=[style_id0]+style_ids


len(style_ids)

soup_styles=BeautifulSoup(archive.open('styles.xml').read(),'lxml')

# styles=soup_styles.find_all('style')
#
# style_ids_1=[st['id'] for st in styles]
#
#
# show=[st for st in style_ids if st in style_ids_1]
#
# show
#
# style_ids
#
# style_ids_1
#
# for st in styles:
#     # if st['id'] not in style_ids:
#     #     st.decompose()
#     print(st['id'])




len(style_ids)



meta=archive.open('meta.xml').read()

zipf=zipfile.ZipFile(r'e:\a\edit.xmind','w')

zipf.writestr('content.xml',soup.prettify(formatter=None))
zipf.writestr('styles.xml',soup_styles.prettify(formatter=None))
zipf.writestr('meta.xml',meta)








#TODO: edit the content.xml directly