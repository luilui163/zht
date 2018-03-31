#-*-coding: utf-8 -*-
#@author:tyhj
from PIL import Image
from pytesseract import pytesseract
import os
import numpy as np
import urllib, cStringIO


def _test():

    fileNames=os.listdir('./captcha')

    filename=fileNames[0]

    im=Image.open('./captcha/%s'%filename)

    im=im.convert('L')

    im.show()

    thresh=125

    table=[]
    for i in range(256):
        if i<thresh:
            table.append(0)
        else:
            table.append(1)

    out=im.point(table,'1')
    out.show()

    text=pytesseract.image_to_string(out)
    print text


def detectCaptcha(content):
    file = cStringIO.StringIO(content)
    im = Image.open(file)
    # im.show()
    im = im.convert('L')
    thresh = 125
    table = []
    for i in range(256):
        if i < thresh:
            table.append(0)
        else:
            table.append(1)
    out = im.point(table, '1')
    # out.show()
    captcha = pytesseract.image_to_string(out)
    return captcha














