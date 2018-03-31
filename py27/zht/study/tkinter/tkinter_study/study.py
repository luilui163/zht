#-*-coding: utf-8 -*-
#@author:tyhj

from Tkinter import *

counter=0
def xinLabel():
    global xin,counter
    counter+=1
    s=Label(xin,text='I love python'+str(counter))
    s.pack()

xin=Tk()
b1=Button(xin,text='tyhj',command=xinLabel)
b1.pack()

xin.mainloop()
#========================================================

from Tkinter import *

xin=Tk()

b1=Button(xin,text='tyhj')
b1['width']=20
b1['height']=4
b1.pack()

b2=Button(xin,text='zht')
b2['width']=20
b2['background']='red'
b2.pack()

xin.mainloop()

#=================================
from Tkinter import *

xin=Tk()
Label(xin,text='user name:').grid(row=0,sticky=W)
Entry(xin).grid(row=0,column=1,sticky=E)

Label(xin,text='password:').grid(row=1,sticky=W)
Entry(xin).grid(row=1,column=1,sticky=E)

Button(xin,text='login').grid(row=2,column=1,sticky=E)
xin.mainloop()

#======================================
from Tkinter import *

def xinlabel(event):
    global xin
    s=Label(xin,text='tyhj')
    s.pack()

xin=Tk()
t=Label(xin,text='simulated button',bg='red')
t.bind('<Button-1>',xinlabel)
t.pack()

xin.mainloop()

#===============================================
from Tkinter import *

def reg():
    s1=e1.get()
    s2=e2.get()
    t1=len(s1)
    t2=len(s2)
    if s1=='111' and s2=='222':
        c['text']='logined in successfully'
    else:
        c['text']='something wrong with user name or password'
        e1.delete(0,t1) #delete those input info
        e2.delete(0,t2)

root=Tk()
l=Label(root,text='user name:')
l.grid(row=0,column=0,sticky=W)

e1=Entry(root)
e1.grid(row=0,column=1,sticky=E)

l2=Label(root,text='password:')
l2.grid(row=1,column=0,sticky=W)

e2=Entry(root)
e2['show']='*'
e2.grid(row=1,column=1,sticky=E)

b=Button(root,text='login',command=reg)
b.grid(row=2,column=1,sticky=E)

c=Label(root,text='')
c.grid(row=3)

root.mainloop()

#======================================
from Tkinter import *

root=Tk()
menubar=Menu(root)
for item in ['file','edit','view','about']:
    menubar.add_command(label=item)

root['menu']=menubar #don't forget about this
root.mainloop()

#===========================================
from Tkinter import *

root=Tk()
menubar=Menu(root)
fmenu=Menu(menubar)
for item in ['new','open','save','save as']:
    fmenu.add_command(label=item)

emenu=Menu(menubar)
for item in ['copy','paste','cut']:
    emenu.add_command(label=item)

vmenu=Menu(menubar)
for item in ['default view','new view']:
    vmenu.add_command(label=item)

amenu=Menu(menubar)
for item in ['copyright infomation','other information']:
    amenu.add_command(label=item)

menubar.add_cascade(label='File',menu=fmenu)
menubar.add_cascade(label='Edit',menu=emenu)
menubar.add_cascade(label='View',menu=vmenu)
menubar.add_cascade(label='About',menu=amenu)

root['menu']=menubar
root.mainloop()

#==================================================
from Tkinter import *

def xin():
    global root
    Label(root,text='I love python').pack()

root=Tk()
menubar=Menu(root)

for x in ['vb','c','java','php']:
    menubar.add_command(label=x)

menubar.add_command(label='python',command=xin)

def pop(event):
    menubar.post(event.x_root,event.y_root)

root.bind('<Button-3>',pop)
root.mainloop()

#====================================================
from Tkinter import *
root=Tk()
m=Menu(root)
m2=Menu(m)
for item in ['python','perl','php','ruby']:
    m2.add_command(label=item)

m2.add_separator()

for item in ['java','c++','c']:
    m2.add_command(label=item)

m.add_cascade(label='lan',menu=m2)
root['menu']=m
root.mainloop()

#====================================================
from Tkinter import *
root=Tk()
m=Menu(root)
m2=Menu(m)
for item in ['python','perl','php','ruby']:
    m2.add_checkbutton(label=item)

m2.add_separator()

for item in ['java','c++','c']:
    m2.add_radiobutton(label=item)

m.add_cascade(label='lan',menu=m2)
root['menu']=m
root.mainloop()

#==============================================
#文本域
from Tkinter import *
root=Tk()
t=Text(root,width=50,height=30)
t.pack()
root.mainloop()

#===================================================
#toplevel
from Tkinter import *
root=Tk()
root.title('root window')
l=Label(root,text='belong to root')
l.pack()

f=Toplevel(root,width=30,height=20)
f.title('toplevel')
lf=Label(f,text='belong to toplevel')
lf.pack()
root.mainloop()

#=========================================================
#canvas
from Tkinter import *
root=Tk()
root.title('canvas')
can=Canvas(root,width=400,height=300,bg='#00FFFF')
can.create_line((0,0),(200,200),width=8)
can.create_text(300,30,text='write something')
can.pack()

root.mainloop()



