#-*-coding: utf-8 -*-
#@author:tyhj

import Tkinter as tk

window=tk.Tk()
window.title('my window')
window.geometry('500x500')

def hit_me():
    tk.messagebox.showinfo(title='Hi',message='hahahahaha')
    tk.Messagebox.showwarning(title='Hi',message='nononono')
    tk.messagebox.showerror(title='Hi',message='No!!never')
    tk.messagebox.showerror(title='Hi',message='hahahaha')
    print tk.messagebox.askquestion(title='Hi',message='hahahaha') #return 'yes','no'
    print tk.messagebox.askyesno(title='Hi', message='hahahaha') #return True or False
    print tk.messagebox.asktrycancel(title='Hi',message='hahahha')
    print tk.messagebox.askokcancel(title='Hi',message='hahahha')

tk.Button(window,text='hit me',command=hit_me).pack()




window.mainloop()












