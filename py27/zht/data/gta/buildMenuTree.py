#-*-coding: utf-8 -*-
#author:tyhj
#buildMenuTree.py 2017/9/6 14:07

import os

import pandas as pd
import numpy as np


def menu1():
    path=r'D:\quantDb\sourceData\gta\data'

    df=pd.read_csv(os.path.join(path,'menuNew1.csv'))

    names=['dbname','DBTitle','NoteTitle','TBTitle']
    df=df[names].drop_duplicates()
    # df=df[:100]
    # df1=df[names].drop_duplicates()
    # df2=df[names[:-1]].drop_duplicates()

    head='\n'.join(open(r'C:\Python27\zht\data\gta\treeTemplate1.html').read().split('\n')[:7])+'\n'
    tail='\n'.join(open(r'C:\Python27\zht\data\gta\treeTemplate1.html').read().split('\n')[-6:])+'\n'

    with open(r'D:\quantDb\sourceData\gta\data\menu1.html','w') as f:
        f.write(head)
        f.write('<ul>\n')
        f.write('\t<li><span class="Collapsable">gta</span><ul>\n')
        g1=df.groupby('dbname')
        for dbname,x1 in list(g1):
            f.write('\t\t<li><span class="Collapsable">%s</span><ul>\n'%dbname)
            g2=x1[names[1:]].groupby('DBTitle')
            for dbtitle,x2 in list(g2):
                f.write('\t\t\t<li><span class="Collapsable">%s</span><ul>\n' % dbtitle)
                g3=x2[names[2:]].groupby('NoteTitle')
                for TBTitle,x3 in list(g3):
                    f.write('\t\t\t\t<li><a class="Collapsable">%s</a><li>\n'% TBTitle)
                f.write('\t\t\t</ul>\n')
                f.write('\t\t\t</li>\n')
            f.write('\t\t</ul>\n')
            f.write('\t\t</li>\n')
        f.write('\t</li>\n')
        f.write('\t</ul>\n')
        f.write('</li>\n')
        f.write('</ul>\n')
        f.write(tail)

    print 'finished'


def menu2():
    path = r'D:\quantDb\sourceData\gta\data'
    df = pd.read_csv(os.path.join(path, 'menuNew1.csv'))

    names = ['dbname', 'DBTitle', 'NoteTitle', 'TBTitle']
    df = df[names].drop_duplicates()
    # df=df[:100]
    # df1=df[names].drop_duplicates()
    # df2=df[names[:-1]].drop_duplicates()

    head = '\n'.join(open(r'C:\Python27\zht\data\gta\treeTemplate2.html').read().split('\n')[:21]) + '\n'
    tail = '\n'.join(open(r'C:\Python27\zht\data\gta\treeTemplate2.html').read().split('\n')[-2:]) + '\n'

    with open(r'D:\quantDb\sourceData\gta\data\menu2.html', 'w') as f:
        f.write(head)
        f.write('<ol class="tree">\n')

        g1 = df.groupby('dbname')
        for dbname, x1 in list(g1):
            f.write('\t<li>\n')
            f.write('\t\t<label>%s</label>\n'%dbname)
            f.write('\t\t<input type="checkbox"/>\n')
            f.write('\t\t<ol>\n')
            g2 = x1[names[1:]].groupby('DBTitle')
            for dbtitle, x2 in list(g2):
                f.write('\t\t<li>\n')
                f.write('\t\t\t<label>%s</label>\n' % dbtitle)
                f.write('\t\t\t<input type="checkbox"/>\n')
                f.write('\t\t\t<ol>\n')
                g3 = x2[names[2:]].groupby('NoteTitle')
                for TBTitle, x3 in list(g3):
                    f.write('\t\t\t\t<li class="file"><a href="">%s</a><li>\n' % TBTitle)
                f.write('\t\t\t</ol>\n')
            f.write('\t\t</ol>\n')

        f.write('\t</li>\n')
        f.write('</ol>')
        f.write(tail)

    print 'finished'


def menu3():
    path = r'D:\quantDb\sourceData\gta\data'
    df = pd.read_csv(os.path.join(path, 'menuNew1.csv'))

    names = ['dbname', 'DBTitle', 'NoteTitle', 'TBTitle', 'Title']
    # df = df[names].drop_duplicates()
    # df=df[:1000]
    # df1=df[names].drop_duplicates()
    # df2=df[names[:-1]].drop_duplicates()

    head = '\n'.join(open(r'C:\Python27\zht\data\gta\treeTemplate2.html').read().split('\n')[:21]) + '\n'
    tail = '\n'.join(open(r'C:\Python27\zht\data\gta\treeTemplate2.html').read().split('\n')[-2:]) + '\n'

    with open(r'D:\quantDb\sourceData\gta\data\menu.html', 'w') as f:
        f.write(head)
        f.write('<ol class="tree">\n')

        g1 = df.groupby('dbname')
        for dbname, x1 in list(g1):
            f.write('\t<li>\n')
            f.write('\t\t<label>%s</label>\n' % dbname)
            f.write('\t\t<input type="checkbox"/>\n')
            f.write('\t\t<ol>\n')
            g2 = x1.groupby('DBTitle')
            for dbtitle, x2 in list(g2):
                f.write('\t\t<li>\n')
                f.write('\t\t\t<label>%s</label>\n' % dbtitle)
                f.write('\t\t\t<input type="checkbox"/>\n')
                f.write('\t\t\t<ol>\n')
                g3 = x2.groupby('NoteTitle')
                for notetitle, x3 in list(g3):
                    f.write('\t\t\t\t<li>\n')
                    f.write('\t\t\t\t\t<label>%s</label>\n' % notetitle)
                    f.write('\t\t\t\t\t<input type="checkbox"/>\n')
                    f.write('\t\t\t\t\t<ol>\n')
                    g4 = x3.groupby('TBTitle')
                    for tbtitle, x4 in list(g4):
                        f.write('\t\t\t\t\t<li>\n')
                        f.write('\t\t\t\t\t\t<label>%s</label>\n' % tbtitle)
                        f.write('\t\t\t\t\t\t<input type="checkbox"/>\n')
                        f.write('\t\t\t\t\t\t<ol>\n')
                        g5 = x4.groupby('Title')
                        for title, x5 in list(g5):
                            f.write('\t\t\t\t\t<li class="file"><a href="file:///D:\\quantDb\\sourceData\\gta\\data\\tablesNew\\%s.csv">%s</a><li>\n' %(x5['TBName'].values[0],title))
                        f.write('\t\t\t\t</ol>\n')
                    f.write('\t\t\t\t</ol>\n')
                f.write('\t\t\t</ol>\n')
            f.write('\t\t</ol>\n')

            print dbname
        f.write('\t</li>\n')
        f.write('</ol>')
        f.write(tail)

    print 'finished'
menu3()
