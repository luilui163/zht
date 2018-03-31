#-*-coding: utf-8 -*-
#@author:tyhj


def dump(obj):
'''output all the obj's properties'''
    for attr in dir(obj):
        print 'obj.%s=%s'%(attr,getattr(obj,attr))















