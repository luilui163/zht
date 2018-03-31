#-*-coding: utf-8 -*-
#@author:tyhj

import sys
import re
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
import pandas as pd


fileName=sys.argv[1]
startPage=int(sys.argv[2])



# fileName='test'
# startPage=31#TODO:change this number for different pdf

#todo:identify the long bookmarks with multiple lines
#todo:from parent to descent
def extractBookmarks():
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
            print 'Extracting bookmark:',chapter+' '+name
    return bookmarks

def saveTocStructure(bookmarks):
    global fileName
    with open(fileName+'_toc.txt','w') as f:
        for b in bookmarks:
            f.write('\t'*b[0]+b[1]+' '+b[2]+'\t'+b[3]+'\n')



def filterBookmarks(bookmarks):
    #filter the bookmarks
    df=pd.DataFrame(bookmarks,columns=['level','chapter','name','page'])
    df['page']=pd.to_numeric(df['page'],errors='coerce')
    df.dropna(axis=0,how='any')

    i=1
    while i<df.shape[0]-1:
       if df.page[i]<df.page[i-1]:
           df.drop(df.index[i],inplace=True)
           df.index=range(len(df))
           # df.reset_index(inplace=True)
       else:
           i+=1

    #add parent chapter
    df['parentChapter']=None
    for i in range(len(df)):
        if '.' in df.chapter[i]:
            parentChapter='.'.join(df.chapter[i].split('.')[:-1])
            # df['parent'][i]='.'.join(df.chapter[i].split('.')[:-1])
            df['parentChapter'][i]=parentChapter
        print 'adding parentChapter',i
    return df

def addBookmarks(bookmarksDf):
    global fileName
    output = PdfFileWriter()
    input1 = PdfFileReader(open(fileName + '.pdf', 'rb'))

    for i in range(input1.getNumPages()):
        output.addPage(input1.getPage(i))

    df['parent']=None
    for i in range(len(df)):
        _,chapter,name,page,parentChapter,parent=df.ix[i]
        title=chapter+' '+name
        if parentChapter is None:
            parent=output.addBookmark(title,page)
            df.loc[(df['parentChapter'] == chapter), 'parent']=parent
        else:
            parent=output.addBookmark(title,page,parent)
            df.loc[(df['parentChapter'] == chapter), 'parent']= parent



    output.write(file(fileName + '_new.pdf', 'wb'))

    # df.to_csv('df3.csv')

if __name__=='__main__':
    bookmarks=extractBookmarks()
    saveTocStructure(bookmarks)
    df=filterBookmarks(bookmarks)
    addBookmarks(bookmarks)
    print 'finished'