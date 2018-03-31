#-*-coding: utf-8 -*-
#@author:tyhj


import PyPDF2

def getPDFContent(path):
    content = ""
    # Load PDF into pyPDF
    pdf = PyPDF2.PdfFileReader(file(path, "rb"))
    # Iterate pages
    for i in range(0, pdf.getNumPages()):
        # Extract text from page and add to content
        content += pdf.getPage(i).extractText() + "\n"
    # Collapse whitespace
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content

print getPDFContent("test.pdf").encode("ascii", "ignore")






