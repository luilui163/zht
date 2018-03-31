#-*-coding: utf-8 -*-
#@author:tyhj

import Tkinter as tk

window=tk.Tk()
window.title('my window')
window.geometry('200x100')

var=tk.StringVar()
textvariable=var
# l=tk.Label(window,text='OMG! this TK!',bg='green',font=('Arial',12),width=15,height=2)
l=tk.Label(window,textvariable=var,bg='green',font=('Arial',12),width=15,height=2)
l.pack()

on_hit=False
def hit_me():
    global on_hit
    if on_hit==False:
        on_hit=True
        var.set('you hit me')
    else:
        on_hit=False
        var.set('')

b=tk.Button(window,text='hit me',width=15,height=2,command=hit_me)

b.pack()

window.mainloop()











