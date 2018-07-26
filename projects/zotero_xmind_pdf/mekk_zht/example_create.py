# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-04  16:34
# NAME:zht-example_create.py

from mekk.xmind import XMindDocument
from zht.projects.zotero_xmind_pdf.mekk_zht import XMindDocument


OUTPUT=r'e:\a\mekk.xmind'

xmind=XMindDocument.create('First sheet title','root subject')
first_sheet=xmind.get_first_sheet()
root_topic=first_sheet.get_root_topic()

root_topic.add_subtopic('first item')
root_topic.add_subtopic('second item')
t=root_topic.add_subtopic('third item')
t.add_subtopic('second level -1')
t.add_subtopic('second level -2')
root_topic.add_subtopic('detached topic',detached=True)
t.add_subtopic('another detached',detached=True)
t.add_marker('flag-red')

# root_topic.doc.doc_tag.remove(t.doc.doc_tag)
test=root_topic.doc.doc_tag

# for ch in test.getchildren():
#     test.remove(ch)


dir(root_topic.doc.doc_tag)



#
#
# import lxml.etree._Element
#
# type(root_topic.doc.doc_tag)
#
# dir(root_topic)
#
# dir(root_topic.doc.doc_tag)
#

root_topic.add_subtopic('link example').set_link('http://mekk.waw.pl')
# root_topic.add_subtopic('attachment example').set_attachment(open('a.py').read(),'.txt')
root_topic.add_subtopic('with note').set_note('''This is just some dummy note.''')

MARKER_CODE = "40g6170ftul9bo17p1r31nqk2a"
# XMP = "../../py_mekk_nozbe2xmind/src/mekk/nozbe2xmind/NozbeIconsMarkerPackage.xmp"
root_topic.add_subtopic(u"With non-standard marker").add_marker(MARKER_CODE)

# xmind.embed_markers(XMP)

xmind.save(OUTPUT)


#xmind.pretty_print()


