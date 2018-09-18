# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-09-12  18:37
# NAME:zht-1.py

def fib(n):
    if n<=2:
        return 1
    else:
        return fib(n-1)+fib(n-2)

# print([fib(i) for i in range(1,21)])

def prime():
    l=[]
    for i in range(2,101):
        for j in range(2,i):
            if i%j==0:
                break
        else:
            l.append(i)
    print(l)


def convert_time_format():
    tc='2014-7-1 13:30:15'
    # ta='7-1-2014 01:30:15'

    [Y,M,D,h,m,s]=[tc.split(' ')[0].split('-')[i] for i in range(3)]+\
                  [tc.split(' ')[1].split(':')[j] for j in range(3)]

    hour=str(int(h)-12) if int(h)-12>=10 else '0'+str(int(h)-12)

    ta=f'{M}-{D}-{Y} {hour}:{m}:{s}'

    seconds=int(h)*3600+int(m)*60+int(s)

    print(ta)
    print(seconds)

convert_time_format()
