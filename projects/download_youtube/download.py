# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-26  22:13
# NAME:zht-download.py

import os

import requests
from bs4 import BeautifulSoup


class Item:
    def __init__(self,iid,url,time,title):
        self.iid=iid
        self.url=url
        self.time=time
        self.title=title
        self.name='{}_{}'.format(iid,title)

proxies={
    'https':'https://127.0.0.1:1080',
    'http':'https://127.0.0.1:1080',
}

header = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

url='https://www.youtube.com/playlist?list=PL8dPuuaLjXtNppY8ZHMPDH5TKK2UpU8Ng'
response=requests.get(url,headers=header,proxies=proxies)

response.text

with open(r'e:\a\text.html','w',encoding='utf8') as f:
    f.write(response.text)


soup=BeautifulSoup(response.text,'lxml')
import re
script=soup.find_all(string=re.compile(r'window\["ytInitialData"\]'))[0]

a=script.split('window["ytInitialPlayerResponse"]')
b=a[0].split('window["ytInitialData"] = ')[1].strip()[:-1]


import json
d=json.loads(b)

contents=d['contents']

plist=contents['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['playlistVideoListRenderer']


import objectpath

jsonn_tree=objectpath.Tree(d)

a=list(jsonn_tree.execute('$..*playlistVideoRenderer'))
b=list(jsonn_tree.execute('$..*videoId'))
b[0]


b[0].keys()
len(a)



jsonn_tree.execute('$.*[1]')

test=jsonn_tree.execute('$.contents')



def download():
    with open(r'e:\a\html.txt',encoding='utf8') as f:
        html=f.read()


    soup=BeautifulSoup(html,'lxml')
    playlist=soup.find_all('ytd-playlist-video-renderer',{'class':'style-scope ytd-playlist-video-list-renderer'})
    rooturl=r'https://www.youtube.com'

    items=[]
    for a in playlist:
        iid=a.find('yt-formatted-string', {'id': 'index'}).text
        url= rooturl + a.find('a', {'class': 'yt-simple-endpoint style-scope ytd-playlist-video-renderer'})['href']
        time=a.find('span', {'class': 'style-scope ytd-thumbnail-overlay-time-status-renderer'}).text.strip()
        title=a.find('span', {'id': 'video-title'}).text.strip()
        items.append(Item(iid,url,time,title))

    directory=r'G:\video\youtube'

    for item in items[:1]:
        print(item.name)
        command = 'you-get -x 127.0.0.1:1080 {url} -O {name} -o {directory}'.format(
            url=item.url, name=item.name, directory=directory)
        os.system(command)



