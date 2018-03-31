# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 21:17:34 2016

@author: hp
"""
from PIL import Image


ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# 将256灰度映射到70个字符上
def get_char(r,b,g,alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]

if __name__ == '__main__':

    im = Image.open(r'C:\Users\hp\Desktop\iii.jpg','r')
    im = im.resize((50,50), Image.NEAREST)

    txt = ""

    for i in range(50):
        for j in range(50):
            txt += get_char(*im.getpixel((j,i)))
        txt += '\n'

    print txt

    #字符画输出到文件

    with open(r'c:\garbage\test.txt','w') as f:
        f.write(txt)

