#-*-coding: utf-8 -*-
#@author:tyhj

import sys
import re
import os

folder=os.getcwd()
startPage=11




content=open(os.path.join(folder,'content.txt'),'r').read()

#use regular expression to match the valid bookmarks and ignore the invalid
lines=content.split('\n')
p=r'[\d]+\s.*\d+$|[\d.]+\s.*\d$'
validLines=[]
for l in lines:
    if re.match(p,l):
        validLines.append(l)
        print l

#standardize the bookmarks
bookmarks=[]
for l in validLines:
    chapter=l.split(' ')[0]
    page=l.split(' ')[-1] #adjust the pages
    contents=l.split(' ')[1:-1]
    #delete the character "."
    validContents=[]
    for c in contents:
        if c!='.':
            validContents.append(c)
    validContents=' '.join(validContents)
    try:
        page = str(startPage-1 + int(page))
        bookmarks.append((chapter,validContents,page))
    except:
        pass




#save bookmarks to the initial txt file
with open(os.path.join(folder,'FreePic2Pdf_bkmk.txt'),'w') as f:
    for b in bookmarks:
        order=b[0].count('.')
        tick='\t'*order+b[0]+' '+b[1]+'\t'+b[2]
        f.write(tick+'\n')










