# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-31  09:42
# NAME:zht-update_tags.py

from mekk.xmind import XMindDocument
import sqlite3

conn=sqlite3.connect(r'D:\zht\database\zoteroDB\zotero.sqlite')
c=conn.cursor()

def query(q):
    c.execute(q)
    return c.fetchall()

def get_tags(iid):
    q0='select itemID from items where key="{}"'.format(iid)
    itemID=query(q0)[0][0]
    q1='select parentItemID from itemAttachments where itemID={}'.format(itemID)
    parentItemID=query(q1)[0][0]
    q2='select tagID from itemTags where itemID={}'.format(parentItemID)
    tagIDs=[i[0] for i in query(q2)]

    q3='select name from tags where tagID={}'
    tags=[query(q3.format(tagID))[0][0] for tagID in tagIDs]
    return tags

def update_tags(path=r'D:\zht\database\xmind\research\reading_papers.xmind'):
    xmind=XMindDocument.open(path)

    sheet=xmind.get_first_sheet()

    sheet.get_title()

    sheets=list(xmind.get_all_sheets())
    summary=[s for s in sheets if 'summary' in s.get_title()][0]

    root=summary.get_root_topic()
    subtopics=root.get_subtopics()

    for sub in subtopics:
        iid=sub.get_link().split('/')[-1]

        if not iid.endswith('.pdf'):
            tags=get_tags(iid)
            sub.set_note('\n'.join(sorted(tags)))
            # sub.set_label(','.join(tags))
            # for tag in tags:
            #     sub.set_label(tag)
        print(iid)

    c.close()
    xmind.save(path)




if __name__ == '__main__':
    update_tags()


