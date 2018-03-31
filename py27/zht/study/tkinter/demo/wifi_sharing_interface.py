#-*-coding: utf-8 -*-
#@author:tyhj
# -*- coding: utf-8 -*-
from Tkinter import *
import tkFont
import os
from PIL import ImageTk, Image

open_wifi_cmd = "netsh wlan start hostednetwork"
close_wifi_cmd = "netsh wlan stop hostednetwork"
message = ''


def show_result(how, cmd):
    global message
    result = os.system(cmd)
    if result != 0:
        if how == 1:
            message.set("请检查无线网卡是否打开，设置是否正确")
        else:
            message.set("关闭WIFI失败！")
    else:
        if how == 1:
            message.set("WIFI已打开")
        else:
            message.set("WIFI已关闭")


def open_wifi():
    cmd = open_wifi_cmd
    show_result(1, cmd)


def close_wifi():
    cmd = close_wifi_cmd
    show_result(0, cmd)


def main():
    root = Tk()
    root.title("WIFI热点小助手");
    # root.geometry('600x400')
    global message
    message = StringVar()
    message.set("Welcome to WIFI Manage!")

    ft = tkFont.Font(family="Arial", size=10, weight=tkFont.BOLD)
    image = Image.open("wifi.gif")
    bm = ImageTk.PhotoImage(image)

    label = Label(root, image=bm)
    label.grid(row=0, columnspan=2)

    open_button = Button(root, text="OPEN", font=ft, pady=5, width=10, borderwidth=2, bg="#F3E9CC", command=open_wifi)
    open_button.grid(row=1, column=0)

    close_button = Button(root, text="CLOSE", font=ft, pady=5, width=10, borderwidth=2, bg="#F3E9CC",
                          command=close_wifi)
    close_button.grid(row=1, column=1)

    status_message = Message(root, textvariable=message, pady=5, width=250)
    status_message.grid(row=2, columnspan=2)

    root.mainloop()


if __name__ == '__main__':
    main()














