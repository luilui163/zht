#-*-coding: utf-8 -*-
#@author:tyhj

import chardet
import os

def decode_the_filenames():
    encoding_types=[]
    directory=r'C:\data\factors'
    filenames=os.listdir(directory)
    for fn in filenames:
        c=chardet.detect(fn)['encoding']
        if c not in encoding_types:
            encoding_types.append(c)


    with open(r'filenames.txt','w') as f:
        for fn in filenames:
            types=[et for et in encoding_types]
            while len(types)>0:
                type=types[0]
                try:
                    fn=fn.decode(type)
                    break
                except:
                    del types[0]
            f.write('%s\n'%fn.encode('utf8'))

def change_filename():
    directory=r'C:\data\factors'
    filenames=os.listdir(directory)
    for fn in filenames:
        files=os.listdir(os.path.join(directory,fn))
        directory1=os.path.join(directory,fn)
        for f in files:
            src=os.path.join(directory1,f)
            dst=os.path.join(directory1,f[:10]+f[-4:])
            os.rename(src,dst)








