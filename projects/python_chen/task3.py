# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-10-23  09:57
# NAME:zht-task3.py
import requests
from bs4 import BeautifulSoup


def get_baidu_news_title(pages=5):
    titles=[]
    for page in range(1,pages+1):
        url=f'http://news.baidu.com/ns?word=%E6%AD%A6%E6%B1%89%E5%A4%A7%E5%AD%A6&pn={page*20}&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0&rsv_page=1'

        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        r=requests.get(url,headers=headers)
        '''
        trick: 如果没有使用 headers 进行伪装成浏览器的话，获取的不是最新的新闻，
        大概又两天的滞后。 这种设定应该是百度为了防止别家新闻网站直接盗用他们的时事新闻。
        '''
        soup=BeautifulSoup(r.text,'lxml')
        results=soup.find_all('div',attrs={'class':'result',})
        for result in results:
            titles.append(result.find_all('a')[0].text.strip())
    with open(r'e:\a\titles.txt','w') as f:
        f.write('\n'.join(titles))

if __name__ == '__main__':
    get_baidu_news_title()

