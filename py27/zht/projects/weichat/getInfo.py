#-*-coding: utf-8 -*-
#author:tyhj
#getInfo.py 2017/8/1 9:06
import pandas as pd
import itchat

itchat.auto_login()


def get_friendsInfo():
    friends=itchat.get_friends(update=True)[0:]
    subdfs=[]
    for f in friends:
        tmp=pd.DataFrame(dict(f).items(),columns=['var','value'])
        tmp=tmp.set_index('var')
        subdfs.append(tmp)

    df=pd.concat(subdfs,axis=1)
    print df
    df=df.T
    df=df.reset_index()
    del df['index']

    df.to_csv('weichatFriends.csv',encoding='utf8')


r=itchat.send('Hello, filehelper', toUserName='@863a622b46cc741785a30ccc1c236a66bdfbc70e341163e906b63ce225ee0030')












