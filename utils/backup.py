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
            zipf.write(os.path.join(subdir,file))
        print(subdir)
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


def split_large_zip(zp, max_size=9 * 1024 * 1024 * 1024):
    '''Split file into pieces, every size is  max_size = 15*1024*1024 Byte'''
    BUF = 50 * 1024 * 1024 * 1024  # 50GB     - memory buffer size

    chapters = 1
    uglybuf = ''
    with open(zp, 'rb') as src:
        while True:
            tgt = open(zp + '.%03d' % chapters, 'wb')
            written = 0
            while written < max_size:
                if len(uglybuf) > 0:
                    tgt.write(uglybuf)
                tgt.write(src.read(min(BUF, max_size - written)))
                written += min(BUF, max_size - written)
                uglybuf = src.read(1)
                if len(uglybuf) == 0:
                    break
            tgt.close()
            if len(uglybuf) == 0:
                break
            chapters += 1
            print(chapters,'finished')

def backup(src, backup_folder=BACKUP_FOLDER, freq=1, history_edition_num=2, max_size=9 * 1024 * 1024 * 1024, force=False):
    now=datetime.now()
    t_format='%Y-%m-%d %H%M%S'
    timestamp=now.strftime(t_format)

    name=os.path.basename(src)
    if len(name)==0:
        if src==r'D:\\':
            name='D'
        else:
            raise ValueError('name is empty!!!')

    newname='{}_{}.zip'.format(name,timestamp)
    dst_zip = os.path.join(backup_folder, newname)
    #TODO: backup or not
    fns=os.listdir(backup_folder)
    fns=[fn for fn in fns if not fn.endswith('.baiduyun.uploading.cfg')]
    parse_time = lambda fn: datetime.strptime(fn[-21:-4], t_format)
    backups=[fn for fn in fns if fn[:-22]==name and fn.endswith('.zip')]

    if len(backups)==0:
        docompress(src,dst_zip)
    else:
        backups=sorted(backups,key=lambda x:parse_time(x))
        last_time = parse_time(backups[-1])
        delta_day = (now - last_time).total_seconds() / (3600 * 24)
        if delta_day >= freq:
            parse_time = lambda fn: datetime.strptime(fn[-21:-4], t_format)
            backups = [fn for fn in fns if fn[:-22] == name and fn.endswith('.zip')]
            backups = sorted(backups, key=lambda x: parse_time(x))
            if len(backups)>history_edition_num-1:
                for bp in backups[:len(backups)-history_edition_num+1]:
                    print('Delete: {}'.format(bp))
                    os.remove(os.path.join(backup_folder,bp))
            docompress(src, dst_zip)
        else:
            if force==True:
                docompress(src,dst_zip)

    if os.path.exists(dst_zip):
        sizeG=os.path.getsize(dst_zip)
        if sizeG>max_size:
            small_bps=[fn for fn in fns if fn[:-22]==name and len(fn.split('.zip')[-1])>0]
            for bp in small_bps:# delete the small .zip files
                os.remove(os.path.join(backup_folder,bp))
            split_large_zip(dst_zip,max_size)


def main():
    srcs = [
        (r'D:\zht\database\xmind', 1,5),
        (r'D:\zht\database\zoteroDB',5,2),#backup every 5 days
        (r'D:\app\python36',1,2),
        (r'D:\zht',10,1),
        (r'G:\backup\software',10,2)
    ]
    for src, freq,num in srcs:
        backup(src,freq=freq,history_edition_num=num)

def debug():
    srcs = [
        (r'D:\zht\database\xmind', 0.00000001, 5),
        (r'D:\app\python36', 0.00000001, 2),
    ]
    for src, freq, num in srcs:
        backup(src, freq=freq, history_edition_num=num,max_size=500*1024*1024)


if __name__ == '__main__':
    main()


