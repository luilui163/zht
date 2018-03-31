#-*-coding: utf-8 -*-
#@author:tyhj

import sys
import re
import os

folder=os.getcwd()
startPage=11#TODO:change this number for different pdf


content=open(os.path.join(folder,'content.txt'),'r').read()
lines=content.split('\n')

#match the bookmarks start with number
#use regular expression to match the valid bookmarks and ignore the invalid
p=r'([0-9|\.]+)(\D.*\D)([0-9]+)'
bookmarks=[]
for l in lines:
    if re.match(p,l):
        m=re.match(p,l)
        chapter,name,page=m.group(1,2,3)

        order = chapter.count('.')

        name=name.replace('.','')
        #TODO: continue to using name=name.replace(invalidChar,'') to delete the other invalid characters
        name=name.strip()

        page=str(int(page)+startPage-1)

        bookmarks.append((order,chapter,name,page))
        print name



with open(os.path.join(folder,'FreePic2Pdf_bkmk.txt'),'w') as f:
    for b in bookmarks:
        f.write('\t'*b[0]+b[1]+' '+b[2]+'\t'+b[3]+'\n')









