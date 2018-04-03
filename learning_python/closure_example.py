# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-02  21:55
# NAME:zht-closure_example.py

import logging
logging.basicConfig(filename='example.log',level=logging.INFO)


def logger(func):
    def log_func(*args):
        logging.info(
            'Running "{}" with arguments {}'.format(func.__name__,args)
        )
        print(func(*args))

    return log_func

def add(x,y):
    return x+y

def sub(x,y):
    return x-y

add_logger=logger(add)
sub_logger=logger(sub)

add_logger(3,3)
add_logger(4,5)

sub_logger(10,5)
sub_logger(20,10)


