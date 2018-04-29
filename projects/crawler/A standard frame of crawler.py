# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-28  19:59
# NAME:zht-A standard frame of crawler.py

import requests

def getHTMLText(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status() # If the status code is not 200,it will raise HTTPError
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return 'Wrong'


if __name__ == '__main__':
    url='http://www.baidu.com'
    print(getHTMLText(url))
