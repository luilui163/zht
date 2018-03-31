#-*-coding: utf-8 -*-
#@author:tyhj

a=1
b=2
if a>1:
    print 'zhanghaitao'
else:
    print 'fudong'


if a>1:
    print 'a>1'
elif b>2:
    print 'b>2'
else:
    print 'zhanghaitao'

for i in range(10):
    print i,'fudong'+"zhanghaitao"



def print_5_times(s):
    for i in range(5):
        print s

print_5_times('fudong')


def if_else(a):
    '''
    a is an int number
    this is an if else function
    author:fudong
    '''
    if a/2==0:
        print a
    elif a/2==1:
        print a+1


if_else(3)

