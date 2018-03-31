# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 16:01:30 2016

@author: Administrator
"""

import re

def get_word_frequence(file_name):
    dic={}
    txt=open(file_name,'r').read().splitlines()
    print txt
    for line in txt:
        line=re.sub(r'[^\u4e00-\u94a5\w\d\-]',' ',line)
        line=re.sub(r"[^a-zA-Z'-]|\\s+|\t|\r",' ',line)
        line=re.sub(r"-{2,}",' ',line)
        line=re.sub(r"'{2,}",' ',line)
        for word in line.split():
            dic.setdefault(word.lower(),0)
            dic[word.lower()]+=1
    li=sorted(dic.iteritems(),key=lambda d:d[1],reverse=True)
    for i in li:
        print i

if __name__=='__main__':
    get_word_frequence(r'c:\python\test.txt')