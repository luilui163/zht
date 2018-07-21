# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-19  20:32
# NAME:zht-example_parse.py

from mekk.xmind import XMindDocument

xmind = XMindDocument.open("test.xmind")

sheet = xmind.get_first_sheet()
print("Sheet title: ", sheet.get_title())

root = sheet.get_root_topic()
print("Root title: ", root.get_title())
print("Root note: ", root.get_note())

for topic in root.get_subtopics():
    print("* ", topic.get_title())
    print("   label: ", topic.get_label())
    print("   link: ", topic.get_link())
    print("   markers: ", list(topic.get_markers()))
    # topic.get_subtopics()

