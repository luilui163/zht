#-*-coding: utf-8 -*-
#@author:tyhj

from pyzotero import zotero


zot=zotero.Zotero('4127316','user','EK5f2IeDcXjAkbZAOrJyRJmW')

items=zot.top(limit=100)

for item in items:
    print 'item type: %s |key:%s'%(item['data']['itemType'],item['data']['key'])








