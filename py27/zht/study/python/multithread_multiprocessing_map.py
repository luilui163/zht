# -*- coding: utf-8 -*-
"""
Created on Fri Aug 05 20:47:21 2016

@author: hp
"""


'''
http://python.jobbole.com/85050/
map函数负责将线程分给不同的CPU。
'''
import urllib2
from multiprocessing.dummy import Pool as ThreadPool

urls = ['http://www.baidu.com','http://www.sina.com','http://www.qq.com']
pool = ThreadPool()
def fun(url):
    content=urllib2.urlopen(url).read()
    return content
results = pool.map(fun,urls)
print results
pool.close()
pool.join()
print 'main ended'