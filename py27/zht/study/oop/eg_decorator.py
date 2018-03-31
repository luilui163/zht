# -*- coding: utf-8 -*-
"""
Created on Sat May 28 15:04:52 2016

@author: Administrator
"""

class BeDeco:
    def be_edit_fun(self):
        print 'source fun.'
    
    def be_keep_fun(self):
        print 'keep fun.'

class Decorator:
    def __init__(self,dec):
        self._dec=dec()
    
    def be_edit_fun(self):
        print 'start...'
        self._dec.be_edit_fun()
    
    def be_keep_fun(self):
        self._dec.be_keep_fun()

if __name__=='__main__':
    bd=BeDeco()
    bd.be_edit_fun()
    bd.be_keep_fun()
    
    dr=Decorator(BeDeco)
    dr.be_edit_fun()
    dr.be_keep_fun()
