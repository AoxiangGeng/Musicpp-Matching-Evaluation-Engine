# -*- coding:utf-8 -*-
from tkinter import *
from PIL import Image, ImageTk
import threading
import time


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg='white')
        self.pack(expand=YES, fill=BOTH)
        self.window_init()
        self.createWidgets()

    def window_init(self):
        self.master.title('MatchingVisualizer')
        width, height = self.master.maxsize()
        self.master.geometry("{}x{}".format(int(width/2), int(height/2)))
        #创建一个toplevel的根窗口，并把他作为擦参数实例化APP对象

    def createWidgets(self):
        # fm1
        self.fm1 = Frame(self)
        self.spButton = Button(self.fm1, text='spbutton')
        self.spButton.pack(side=LEFT)
        load = Image.open('/Users/jiating/Desktop/ppaa/sc.png')
        render = ImageTk.PhotoImage(load)
        self.img = Label(self.fm1, image=render)
        self.img.image = render
        self.img.pack()
        self.fm1.pack(side=TOP)

        self.fm2 = Frame(self)
        self.tppButton = Button(self.fm2, text='tppbutton')
        self.tppButton.pack(side=LEFT)
        load = Image.open('/Users/jiating/Desktop/ppaa/sc.png')
        render = ImageTk.PhotoImage(load)
        self.img = Label(self.fm2, image=render)
        self.img.image = render
        self.img.pack()
        self.fm2.pack(side=TOP)


        # self.tpButton = Button(self.fm1_left_down, text='tpbutton')
        # self.tpButton.pack(side=TOP)
        # self.fm1.pack(side=LEFT)

        # fm2
        #

        # self.img = Label(self.fm1_left_up , image=render)
        #
        #
        #


if __name__=='__main__':
    app = Application()
    app.mainloop()