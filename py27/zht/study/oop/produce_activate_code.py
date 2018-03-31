# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 16:01:30 2016

@author: Administrator
"""

import random
import string

def activation_code(mark,length=10):
    prefix=hex(int(mark))+'L'
    length=length-len(prefix)
    chars=string.ascii_letters+string.digits
    return prefix+''.join([random.choice(chars) for i in range(length)])
    
def get_mark(code):
    return str(int(code.upper(),16))

if __name__=='__main__':
    for i in range(400,1100,35):
        code=activation_code(i)
        mark_hex=code.split('L')[0]
        mark=get_mark(mark_hex)
        print code,mark
