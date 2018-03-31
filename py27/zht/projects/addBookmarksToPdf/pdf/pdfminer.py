#!python
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

pdf_path='test.pdf'

infile = open(pdf_path, 'rb')
parser = PDFParser(infile)
document = PDFDocument(parser)

toc = list()
for (level,title,dest,a,structelem) in document.get_outlines():
    toc.append((level, title))



