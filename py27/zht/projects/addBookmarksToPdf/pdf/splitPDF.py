#-*-coding: utf-8 -*-
#@author:tyhj
from PyPDF2 import PdfFileWriter, PdfFileReader


fileName='test'
startPage=7
endPage=12



output=PdfFileWriter()
input=PdfFileReader(open(fileName+'.pdf','rb'))

for i in range(startPage-1,endPage):
    output.addPage(input.getPage(i))

output.write(file(fileName+'_'+str(startPage)+'_'+str(endPage)+'.pdf','wb'))

print 'split finished'






