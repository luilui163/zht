# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-09-16  10:35
# NAME:assetPricing2-tool.py

def add_suffix_for_sid(s):
    '''There are some codes whose initial number is 2 or 9 '''
    print('Warning!!!!  add_suffix_for_sid may have some bugs')
    #fixme: use data from wind or gta to identify the suffix rather than search on internet and add suffix based on the initial character of the stock code
    def _for_one_str(s):
        if len(s) == 6:
            if s[0] in ['0','3']:
                return s+'.SZ'
            elif s[0] in ['6']:
                return s+'.SH'
            # if s.startswith('3'):
            #     return s + '.SZ'
            # else:
            #     return s + '.SH'
        else:
            return '0' * (6 - len(s)) + s + '.SZ'

    if isinstance(s,str):
        return _for_one_str(s)
    else:
        return [_for_one_str(ele) for ele in s]
