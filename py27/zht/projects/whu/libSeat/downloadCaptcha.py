#-*-coding: utf-8 -*-
#@author:tyhj

import urllib
import time
import hashlib
from PIL import Image
import os


url=r'http://seat.lib.whu.edu.cn/simpleCaptcha/captcha'
for i in range(100):
    m=hashlib.md5()
    m.update('%s%s'%(time.time(),i))
    name=m.hexdigest()
    urllib.urlretrieve(url,'./captcha/%s.gif'%name)
    print i

imgs=os.listdir('./captcha')


for i,img in enumerate(imgs):
    im=Image.open('./captcha/%s'%img)
    im=im.convert('P')
    im2 = Image.new('P', im.size, 255)
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pix = im.getpixel((x, y))
            if pix ==0:# TODO: or pix<threshold
                im2.putpixel((x, y), 0)
    im2.save('./newcaptcha/%s.gif' % img)
    print i


#split the characters

# imgs=os.listdir('./newCaptcha')
# for i,img in enumerate(imgs):
#     im=Image.open('./newCaptcha/%s'%img)
#     for x in range(im.size[0]):
#         for y in range(im.size[1]):
#             pix=im.getpixel((x,y))


imgs=os.listdir('./newCaptcha')
img=imgs[0]
im=Image.open('./newCaptcha/%s'%img)

# from collections import Counter
# count=Counter(im.histogram())
#
# print count


withLetter=[False]*im.size[0]
for x in range(im.size[0]):
    for y in range(im.size[1]):
        pix=im.getpixel((x,y))
        print pix
        if pix==0:
            withLetter[x]=True

print withLetter


str=''.join(['1' if l else '0' for l in withLetter])
print str



import hashlib
import time

letters=[]
start=False
end=False
newWithLetter=[False]*len(withLetter)
for i in range(1,len(withLetter)-1):


    if not withLetter[i-1] and withLetter[i]:
        newWithLetter='start'
        start=i
    if start and withLetter[i] and not withLetter[i+1]:
        newWithLetter='end'
        end=i
        if end-start>14:
            letters.append((start,end))


print letters


import hashlib
import time

count=0

for i,letter in enumerate(letters):
    im1=im.crop((letter[0],0,letter[1],im.size[1]))
    im1.save('./characters/%s.gif'%(i))
    print letter[1]-letter[0]

# for letter in letters:
#     m=hashlib.md5()
#     im1=im.crop((letter[0],0,letter[1],im.size[1]))
#     m.update('%s%s'%(time.time(),count))
#     im1.save('./characters/%s.gif'%(m.hexdigest()))
#     count+=1







