#-*-coding: utf-8 -*-
#@author:tyhj
import textract

text= textract.process('test_7_12.pdf')



with open('test_7_12.txt','w') as f:
    f.write(text)


print 'finished'


import slate
with open('test_7_12.pdf') as f:
    doc=slate.PDF(f)
print doc
# with open('test_7_12.txt','w') as f:
#     f.write()



