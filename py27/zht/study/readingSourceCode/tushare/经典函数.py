# -*-coding: utf-8 -*-
# author:tyhj
# 经典函数.py 2017/9/30 22:46
import sys

INDEX_LABELS = ['sh', 'sz', 'hs300', 'sz50', 'cyb', 'zxb', 'zx300', 'zh500']
INDEX_LIST = {'sh': 'sh000001', 'sz': 'sz399001', 'hs300': 'sh000300',
              'sz50': 'sh000016', 'zxb': 'sz399005', 'cyb': 'sz399006',
              'zx300': 'sz399008', 'zh500': 'sh000905'}


def _code_to_symbol(code):
    '''
        生成代码标志

    Args:
        code:

    Returns:

    '''
    if code in INDEX_LABELS:
        return INDEX_LIST[code]
    else:
        if len(code) != 6:
            return code
        else:
            return 'sh%s' % code if code[:1] in ['5', '6', '9'] else 'sz%s' % code


class Person:
    def __init__(self):
        """
        Returns:
            object: 

        """

info = sys.version_info

a = choice(range(10))

dict{a=5}