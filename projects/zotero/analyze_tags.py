# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-06-28  00:13
# NAME:zht-analyze_tags.py

from pyzotero import zotero

library_id=4127316
api_key='JpLmWYy5sIRuqbUwwZXDTfxm'

zot=zotero.Zotero(library_id=library_id,library_type='user',api_key=api_key)
items=zot.top(limit=5)
for item in items:
    print('Item: %s | key: %s'% (item['data'],item['data']['key']))



zot.key_info()
zot.groups()
result=zot.everything(zot.top())

dir(zot)


tags=zot.tags()
len(tags)

zot.item_tags()

tags=sorted(tags)
tags
#TOD    O:read sqlite directly from local disk


