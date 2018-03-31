# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-12  11:38
# NAME:assetPricing-a.py

def test_try(a):
    try:
        raise SyntaxError
    except:
        print('daf')

def add_a_new_function():
    pass


if __name__=='__main__':
    test_try(5)
