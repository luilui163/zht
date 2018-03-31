#-*-coding: utf-8 -*-
#@author:tyhj

import Tkinter as tk

window=tk.Tk()
window.title('my window')
window.geometry('500x500')

# tk.Label(window,text=1).pack(side='top')
# tk.Label(window,text=1).pack(side='bottom')
# tk.Label(window,text=1).pack(side='left')
# tk.Label(window,text=1).pack(side='right')
#
# tk.Label(window,text=1).place(x=10,y=100,anchor='nw')

for i in range(4):
    for j in range(3):
        tk.Label(window,text=1).grid(row=i,column=j,padx=10,pady=10)
        print i,j


window.mainloop()









