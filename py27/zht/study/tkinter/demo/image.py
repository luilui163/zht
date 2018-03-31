#-*-coding: utf-8 -*-
#@author:tyhj


from Tkinter import *

root = Tk()
cv = Canvas(root, bg='white', width=500, height=650)
rt = cv.create_rectangle(10, 10, 110, 110, outline='red', stipple='gray12', fill='green')
imgs = [PhotoImage(file='c:\\' + str(i) + '.gif') for i in range(1,3)]
for img in imgs:
    cv.create_image((20 * i, 200 * i), image=img)
cv.pack()
root.mainloop()













