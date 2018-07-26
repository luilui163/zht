# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-25  13:48
# NAME:zht-backup.py


import os
import zipfile
import shutil
from datetime import datetime

BACKUP_FOLDER=r'G:\backup\backup_automatically'

def docompress(src, dst_zip):
    '''
    copy files and folder and compress into a zip file
    :param src:
    :param dst_zip:
    :return:
    '''
    zipf=zipfile.ZipFile(dst_zip, 'w')
    for subdir,dirs,files in os.walk(src):
        for file in files:
            print(os.path.join(subdir,file))
            zipf.write(os.path.join(subdir,file))
    print('Created ', dst_zip)

def docopy(src, dst):
    '''
    copy files to a target folder
    :param src:
    :param dst:
    :return:
    '''
    shutil.copytree(src, dst)
    print('Copy finished')

def backup(src,backup_folder=BACKUP_FOLDER,freq=1,history_edition_num=5):
    now=datetime.now()
    t_format='%Y-%m-%d %H%M%S'
    timestamp=now.strftime(t_format)

    name=os.path.basename(src)
    newname='{}_{}.zip'.format(name,timestamp)

    fns=os.listdir(backup_folder)
    backup_files=[fn for fn in fns if fn.startswith(name)]
    if len(backup_files)>history_edition_num:
        for fn in backup_files[:len(backup_files)-history_edition_num]:
            print('Delete: {}'.format(fn))
            os.remove(os.path.join(backup_folder,fn))

    parse_time=lambda fn:datetime.strptime(fn.split('_')[-1][:-4],t_format)
    # backup_files=[(fn,os.path.getmtime(os.path.join(backup_folder,fn)) for fn in fns)]
    backup_files=sorted(backup_files,key=parse_time)

    latest=backup_files[-1]
    last_time=parse_time(latest)
    delta_day=(now-last_time).total_seconds()/(3600*24)
    if delta_day>=freq:
        dst_zip=os.path.join(backup_folder,newname)
        docompress(src,dst_zip)

def main():
    srcs = [
        (r'D:\zht\database\xmind', 1),
        (r'D:\zht\database\docearDB',1)
    ]
    for src, freq in srcs:
        backup(src,freq=freq)


if __name__ == '__main__':
    main()

