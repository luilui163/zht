#-*-coding: utf-8 -*-
#@author:tyhj
import urllib
import time
import hashlib
from PIL import Image
import os
from pytesseract import pytesseract



imgs=os.listdir('./Captcha')
img=imgs[0]
im=Image.open('./Captcha/%s'%img)
im=im.convert('L')

im1=im.crop((9,0,im.size[0]-9,im.size[0]))
im2=im.crop((9,10,im.size[0]-9,im.size[0]-10))


s=pytesseract.image_to_string(im)
# a=pytesseract.image_to_string(im1)
# b=pytesseract.image_to_string(im2)

print s


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
















