# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 18:41:31 2016

@author: hp
"""

#splitting strings on any of mutiple delimiters
line='adsf gdj; dsad, gdk,as,    foo'
import re
l=re.split(r'[;,\s]\s*',line)
print l  #['adsf', 'gdj', 'dsad', 'gdk', 'as', 'foo']



choices=('http:','ftp:')
url='http://www.python.org'
url.startswith(choices)


#matching and searching for text patterns
text1='11/27/2015'
text2='Nov 27, 2015'

import re
p=re.compile(r'\d+/\d+/\d+')
if p.match(text1):
    print 'yes'
else:
    print 'no'

text='Today is 11/27/2016. PyCon starts 3/13/2013.'
date=p.findall(text)
print date #['11/27/2016', '3/13/2013']


#searching and replacing text
text='Today is 11/27/2016. PyCon starts 3/13/2013.'
text_formatted=re.sub(r'(\d+)/(\d+)/(\d+)',r'\3-\1-\2',text)
print text_formatted#Today is 2016-11-27. PyCon starts 2013-3-13.
'''
The first argument to sub() is the pattern to match and the second
argument is the replacement pattern.Blackslashed digits such as \3 
refer to capture group numbers in the pattern
'''


#stripping unwanted characters from strings

s='   hello world \n'
s.strip()
s.lstrip()
s.rstrip()

t='------hello======'
t.strip('=-')


s='   hello         world  \n'
s=s.strip()
import re
s=re.sub(r'\s+',' ',s)
print s


#Aligning text strings
text='hello world'
print text.ljust(20)
print text.rjust(20)
print text.center(20)

print text.rjust(20,'=')
print text.center(20,'*')



#reformatting text to a fixed number of columns
s='look in to my eyes,look in to my look in to my eyes,look in to my, \
look in to my eyes,look in to mylook in to my eyes,look in to my \
look in to my eyes,look in to mylook in to my eyes,look in to my \
look in to my eyes,look in to my'

import textwrap
print textwrap.fill(s,20)
print textwrap.fill(s,30,initial_indent='    ')
print textwrap.fill(s,30,subsequent_indent='    ')











