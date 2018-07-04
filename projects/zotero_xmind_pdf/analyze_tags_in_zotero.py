# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-06-28  00:13
# NAME:zht-analyze_tags_in_zotero.py
from collections import Counter

import bibtexparser
from pyzotero import zotero

def by_pyzotero():
    library_id=4127316
    api_key='JpLmWYy5sIRuqbUwwZXDTfxm'

    zot=zotero.Zotero(library_id=library_id,library_type='user',api_key=api_key)

    tags=zot.tags(limit=1000)

    len(tags)

    zot.num_tagitems(tags[1])


def by_sqlite3():
    import sqlite3
    conn = sqlite3.connect(r'e:\a\zotero.sqlite')
    c = conn.cursor()
    def query(q):
        c.execute(q)
        return c.fetchall()


def by_bibtex():
    import pandas as pd
    data=pd.read_csv(r'e:\zotero.csv')
    manual_tags=data['Manual Tags']
    # automatic_tags=df['Automatic Tags']

    ab=manual_tags.str.split('; ').dropna().sum()
    count=Counter(ab)
    tc=tuple(zip(count.keys(), count.values()))
    tag_df=pd.DataFrame(list(tc),columns=['tags','count'])
    tag_df=tag_df.sort_values('tags').reset_index(drop=True)
    tag_df.to_csv(r'e:\a\tag_df.csv',encoding='gbk')

by_bibtex()
