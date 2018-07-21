# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-19  20:30
# NAME:zht-split.py
import os

import xmind
from xmind.core import workbook,saver
from xmind.core.topic import TopicElement

fp=r'e:\a\reading papers.xmind'
dir_output=r'e:\a\test'

w=xmind.load(fp)
s=w.getPrimarySheet()
r=s.getRootTopic()

paper_topic=r.getSubTopics()[0]


w = xmind.load(
    r"e:\a\test.xmind")  # load an existing file or create a new workbook if nothing is found
s1 = w.getPrimarySheet()  # get the first sheet
s1.setTitle("first sheet")  # set its title
r1 = s1.getRootTopic()  # get the root topic of this sheet
r1.setTitle("we don't care of this sheet")  # set its title


s2 = w.createSheet()  # create a new sheet
s2.setTitle("second sheet")
r2 = s2.getRootTopic()
r2.setTitle("root node")
t=r2.addSubTopic()
t.setTitle('t')

r2.appendChild(t)



# r2.removeChild(t)


# t1 = r2.addSubTopic()
# t1.setTopicHyperlink(s1.getID())
# t1.setTitle("redirection to the first sheet")  # set its title

xmind.save(w, r"e:\a\test2.xmind")






#
# iid=t1.getHyperlink().split('/')[0]
# name=t1.getTitle()[:-4]
#
# nw=xmind.load(os.path.join(dir_output,name+'.xmind'))
# s=nw.getPrimarySheet()
# s.setTitle('annotations')
# r=s.getRootTopic()
# r.setTitle(iid)
#
# s2=w.createSheet()
# s2.setTitle('second sheet')
# r2=s2.getRootTopic()
# r2.setTitle('root node')
#
#
# t2=TopicElement()
# t2.setTitle('test')
#
#
# r2.addSubTopic(t2)
# xmind.save(w,os.path.join(dir_output,name+'.xmind'))





