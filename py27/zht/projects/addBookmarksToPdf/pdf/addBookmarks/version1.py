#-*-coding: utf-8 -*-
#@author:tyhj

import sys
import re
import os
from pypdf2_notes import PdfFileWriter, PdfFileReader


fileName=sys.argv[1]
startPage=int(sys.argv[2])



# fileName='test'
# startPage=31#TODO:change this number for different pdf

#todo:identify the long bookmarks with multiple lines
#todo:from parent to descent
def extract_bookmarks():
    global fileName,startPage
    directory=os.getcwd()
    content=open(os.path.join(directory,fileName+'.txt'),'r').read()
    lines=content.split('\n')

    #match the bookmarks start with number
    #use regular expression to match the valid bookmarks and ignore the invalid
    p=r'([0-9|\.]+)(\D.*\D)([0-9]+)'
    bookmarks=[]
    for l in lines:
        if re.match(p,l):
            m=re.match(p,l)
            chapter,name,page=m.group(1,2,3)

            level = chapter.count('.')

            name=name.replace('.','')
            #TODO: continue to using name=name.replace(invalidChar,'') to delete the other invalid characters
            name=name.strip()

            page=str(int(page)+startPage-1)

            bookmarks.append((level,chapter,name,page))
            print 'Extracting bookmark:',chapter+name
    return bookmarks

def get_standardized_toc(bookmarks):
    global fileName
    with open(fileName+'_toc.txt','w') as f:
        for b in bookmarks:
            f.write('\t'*b[0]+b[1]+' '+b[2]+'\t'+b[3]+'\n')



def add_bookmarks(bookmarks):
    global fileName
    global directory

    directory=os.getcwd()

    output = PdfFileWriter()
    input1 = PdfFileReader(open(os.path.join(directory,fileName+'.pdf'), 'rb'))

    # output.cloneReaderDocumentRoot(input1)
    for i in range(input1.getNumPages()):
        output.addPage(input1.getPage(i))

    level,chapter,name,page=bookmarks[0]
    title=chapter+' '+name
    page=int(page)
    parent1=output.addBookmark(title,page)

    for i in range(1,len(bookmarks)-1):
        level,chapter,name,page=bookmarks[i]
        title=chapter+' '+name
        page=int(page)
        if level>bookmarks[i-1][0]:
            parent2=output.addBookmark(title,page,parent1)
        elif level==bookmarks[i-1][0]:
            parent2=output.addBookmark(title,page,parent1)
        elif level<bookmarks[i-1][0]:
            parent1=output.addBookmark(title,page)
        print 'add bookmarks ',title
    output.write(file(fileName+'_new.pdf','wb'))


if __name__=='__main__':
    bookmarks = extract_bookmarks()
    get_standardized_toc(bookmarks)
    add_bookmarks(bookmarks)
    print 'complete'







