#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 16:50:55 2019

@author: alex
"""

import tkinter as tk
import pygame.mixer as mixer
import tkinter.filedialog
import app
import numpy as np
from PIL import Image, ImageTk, ImageGrab 
#import sys, os
#import numpy as np
#from pitchogram import pitchogram_from_signal
#from wave_signal import Signal
#import wave
#import matplotlib as plt
#sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

"""
主体部分
"""

window = tk.Tk()
window.title("MusicPP Matching 评估器 ")
window.geometry('1800x1600')
#欢迎语句：
L1 = tk.Label(window,text='欢迎使用和弦佳佳Matching评估器!',bg='lightblue',
             fg='white',font=('Arial',20),width=100,height=5).pack(side='top',fill='x')

#生成主frame
frame = tk.Frame(window)
#生成子frames：
frame1 = tk.Frame(frame,width=1500,height=200).pack(side='top',fill='x',expand=False)
frame2 = tk.Frame(frame,width=1500,height=200).pack(side='bottom',fill='x',expand=False)


#设定字符变量var1，var2
var1 = tk.StringVar()
var1.set('请选择wav文件')
var2 = tk.StringVar()
var2.set('请选择wav文件')
#设定label-L2 ，L3，用来显示var1,var2的信息
L2 = tk.Label(frame1, textvariable=var1,bg='blue',fg='white',font=('Arial',10),width=35,height=5).place(anchor='e',x=350,y=300)
L3 = tk.Label(frame2, textvariable=var2,bg='blue',fg='white',font=('Arial',10),width=35,height=5).place(anchor='e',x=350,y=650)

#两个音频文件的默认名称：
filename1 = 'sp_cut.wav'
filename2 = 'tp_cut.wav'

#临时函数，用于测试
def do_job():
    pass
#二分法查找,返回与检测值t对应的TP_index，或是最近元素的index，若是最近的元素与检测值相差超过0.05s， 则返回 None:  
def binary_search(array,t):
    t = float(t)
    low = 0
    height = len(array)-1
    while low <= height:
        mid = (low+height)//2
        
        if float(array[mid]) < t:
            low = mid+1

        elif float(array[mid]) > t:
            height = mid-1 

        else:
            return array.index(array[mid])
    
    distance1 = abs(float(array[height]) - t)
    try:
        distance2 = abs(float(array[low])-t)
    except IndexError:
        print('Has reached the end of this audio file!')
        return array.index(array[height])

    if distance1 < distance2 and distance1 <= 0.05:
        return array.index(array[height])
    elif distance2 <= distance1 and distance2 <= 0.05:
        return array.index(array[low])
    else:
        return None
    
#input函数用于导入音频文件,由用户选择文件，然后该函数获得文件的路径，将路径存储为filename1和filename2：
def input_wav1():
    global filename1
    filename1 = tk.filedialog.askopenfilename()
    if filename1 != '':
        var1.set("文件加载成功")
    else:
        var1.set("您没有选择任何文件")
def input_wav2():
    global filename2
    filename2 = tk.filedialog.askopenfilename()
    if filename2 != '':
        var2.set("文件加载成功")
    else:
        var2.set("您没有选择任何文件")

#两个Button用于导入音频文件：       
B1 = tk.Button(frame1,text='请选择sp_wav文件',command=input_wav1).place(anchor='w',x=200,y=170)
B2 = tk.Button(frame2,text='请选择tp_wav文件',command=input_wav2).place(anchor='w',x=200,y=520)
"""
Zoom
"""
class LoadImage: 
    def __init__(self,root): 
     frame = tk.Frame(root) 
     self.canvas = tk.Canvas(frame,width=1800,height=2000,scrollregion=(0,0,3500,3000)) 
     self.hscroll = tk.Scrollbar(root,orient='horizontal',bd=2)
     self.hscroll.config(command=self.canvas.xview)
     self.canvas.config(xscrollcommand=self.hscroll.set)
     self.hscroll.pack(side='bottom',fill='x')
     self.vscroll = tk.Scrollbar(root,orient='vertical',bd=2)
     self.vscroll.config(command=self.canvas.yview)
     self.canvas.config(yscrollcommand=self.vscroll.set)
     self.vscroll.pack(side='left',fill='y')
     self.canvas.pack() 
     frame.pack() 
     File = "cut.png" 
     self.orig_img = Image.open(File)
     self.img = ImageTk.PhotoImage(self.orig_img) 
     self.canvas.create_image(0,0,image=self.img, anchor="nw") 

     self.zoomcycle = 0 
     self.zimg_id = None 

     root.bind("<MouseWheel>",self.zoomer) 
     self.canvas.bind("<Motion>",self.crop) 

    def zoomer(self,event): 
     if (event.delta > 0): 
      if self.zoomcycle != 4: self.zoomcycle += 1 
     elif (event.delta < 0): 
      if self.zoomcycle != 0: self.zoomcycle -= 1 
     self.crop(event) 

    def crop(self,event): 
     if self.zimg_id: self.canvas.delete(self.zimg_id) 
     if (self.zoomcycle) != 0: 
      x,y = event.x, event.y 
      if self.zoomcycle == 1: 
       tmp = self.orig_img.crop((x-45,y-30,x+45,y+30)) 
      elif self.zoomcycle == 2: 
       tmp = self.orig_img.crop((x-30,y-20,x+30,y+20)) 
      elif self.zoomcycle == 3: 
       tmp = self.orig_img.crop((x-15,y-10,x+15,y+10)) 
      elif self.zoomcycle == 4: 
       tmp = self.orig_img.crop((x-6,y-4,x+6,y+4)) 
      size = 300,200 
      self.zimg = ImageTk.PhotoImage(tmp.resize(size)) 
      self.zimg_id = self.canvas.create_image(event.x,event.y,image=self.zimg) 
def zoom():
    root = tk.Toplevel()
    root.geometry('1800x1000')
    cut = ImageGrab.grab()
    cut.save('cut.png')
    root.title("Crop Test") 
    App = LoadImage(root)
    root.mainloop() 
"""
设置Menu部分：
"""

menubar = tk.Menu(window)

#设置Filemenu
filemenu = tk.Menu(menubar,tearoff=0)
#加载filemenu到menubar
menubar.add_cascade(label='File',menu=filemenu)

#设置fimemenu中的选项--new，open，save：
filemenu.add_command(label='New', command=do_job)
filemenu.add_command(label='Open', command=do_job)
filemenu.add_command(label='Save', command=do_job)
#插入一个分隔符
filemenu.add_separator()
#在filemenu的最后插入一个exit选项
filemenu.add_command(label='Exit',command=window.quit())

#设置Editmenu
editmenu = tk.Menu(menubar,tearoff=0)
#加载editmenu到menubar
menubar.add_cascade(label='Edit',menu=editmenu)
#设置editmenu中的选项--cut，copy，paste：
editmenu.add_command(label='Zoom', command=zoom)
editmenu.add_command(label='Copy', command=do_job)
editmenu.add_command(label='Paste', command=do_job)

#在filemenu中加一个子menu--import：
submenu = tk.Menu(filemenu)
filemenu.add_cascade(label='Import',command=do_job)
submenu.add_command(label='Submenu_1', command=do_job) 

#将设置好的menu展示出来：
window.config(menu=menubar)



"""
设置音频播放
"""
#初始化播放环境：
mixer.init()

#用于sp的 播放，停止，暂停三个函数：
def track_start1():
    channel1.play(track1,loops = -1)
 
def track_stop1():
    channel1.stop()

pause = False
def track_pause1():
    global pause
    if pause == False:
        channel1.pause()
        pause = True
    else:
        channel1.unpause()
        pause = False

#sp命名为track1，并将channel1分配给它：
channel1 = mixer.Channel(1)
track1 = mixer.Sound(filename1)

#用于sp的 播放，停止，暂停三个按钮：
start_button1 = tk.Button(frame1,command = track_start1,text = "Start")
start_button1.place(anchor='w',x=200,y=190)
stop_button1 = tk.Button(frame1,command = track_stop1,text = "Stop")
stop_button1.place(anchor='w',x=200,y=210)
pause_button1 = tk.Button(frame1,command = track_pause1,text = "Pause")
pause_button1.place(anchor='w',x=200,y=230)


#用于tp的 播放，停止，暂停三个函数：
def track_start2():
    channel2.play(track2,loops = -1)
 
def track_stop2():
    channel2.stop()

pause = False
def track_pause2():
    global pause
    if pause == False:
        channel2.pause()
        pause = True
    else:
        channel2.unpause()
        pause = False

#tp命名为track2，并将channel2分配给它：
channel2 = mixer.Channel(2)
track2 = mixer.Sound(filename2)
#用于tp的 播放，停止，暂停三个按钮：
start_button2 = tk.Button(frame2,command = track_start1,text = "Start")
start_button2.place(anchor='w',x=200,y=540)
stop_button2 = tk.Button(frame2,command = track_stop1,text = "Stop")
stop_button2.place(anchor='w',x=200,y=560)
pause_button2 = tk.Button(frame2,command = track_pause1,text = "Pause")
pause_button2.place(anchor='w',x=200,y=580)


"""
频谱图部分
"""


#sp频谱图画布 canvas1:
canvas1 = tk.Canvas(frame1,bg='gray',width=900,height=390,scrollregion=(0,0,20000,8000),xscrollincrement=0.1)
hbar1 = tk.Scrollbar(frame1,orient='horizontal',bd=0)
hbar1.config(command=canvas1.xview)
canvas1.config(xscrollcommand=hbar1.set)




#tp频谱图画布 canvas2:
canvas2 = tk.Canvas(frame2,bg='gray',width=900,height=390,scrollregion=(0,0,20000,8000),xscrollincrement=0.1)
hbar2 = tk.Scrollbar(frame2,orient='horizontal',bd=0)
hbar2.config(command=canvas2.xview)
canvas2.config(xscrollcommand=hbar2.set)


#生成的频谱图将以默认的名字 img1&img2 保存在当前目录下：
img1 = 'sp.png'
img2 = 'tp.png'
#用于生成频谱图的函数
length1 = 0.0
def generate_specgram1():
    global img1
    global filename1
    #必须将PhotoImage指定的tempImage声明为全局变量，否则图片在canvas中将不会被显示
    global tempImage1
    global length1
    showpic = app.Draw_pic(filename1,img1)
    #threshold:0-1; darkness:0-9
    length1 = showpic.energypic(0.9,9)
    #根据频谱图的长度调整canvas的窗口长度
    canvas1.config(scrollregion=(0,0,length1,8000))
    tempImage1 = tk.PhotoImage(file = img1)
    canvas1.create_image(0, 194,anchor='w',image=tempImage1)
#    canvas1.show()
#    canvas1.FigureCanvasTkAgg(tempImage1,master=frame1)
    
def generate_specgram2():
    global img2
    global filename2
    #必须将PhotoImage指定的tempImage声明为全局变量，否则图片在canvas中将不会被显示
    global tempImage2
    showpic = app.Draw_pic(filename2,img2)
    length2 = showpic.energypic(0.9,9)
    #根据频谱图的长度调整canvas的窗口长度
    canvas2.config(scrollregion=(0,0,length2,8000))
    tempImage2 = tk.PhotoImage(file = img2)
    canvas2.create_image(0, 194,anchor='w',image=tempImage2)
#    canvas2.show()
#    canvas2.FigureCanvasTkAgg(tempImage2,master=frame2)

#用于生成频谱图的两个按钮：
B_sp = tk.Button(frame1,text = "绘制",command=generate_specgram1)
B_tp = tk.Button(frame2,text = "绘制",command=generate_specgram2)
B_sp.place(anchor='w',x=200,y=250)
B_tp.place(anchor='w',x=200,y=600)
#canvas1.bind('<Button-1>',specgram1)
#canvas2.bind('<KeyPress-p>',specgram2)
#放置scrollbar-- hbar1 & hbar2至窗口底部，并铺满整个x轴:
hbar2.pack(side='bottom',fill='x')
hbar1.pack(side='bottom',fill='x')
canvas1.place(anchor='w',x=350,y=340)
canvas2.place(anchor='w',x=350,y=690)

"""
Match部分
"""

#match文件的默认地址：
filename3 = 'sp_cut_tp_match.csv'

var3 = tk.StringVar()
var3.set('请选择match.csv文件')
#导入match数据：
def input_csv():
    global filename3
    filename3 = tk.filedialog.askopenfilename()
    if filename3 != '':
        var3.set("文件加载成功")
    else:
        var3.set("您没有选择任何文件")
        
#提示导入match文件并显示其路径：        
L4 = tk.Label(frame2, textvariable=var3,bg='blue',fg='white',font=('Arial',10),width=35,height=5).place(anchor='w',x=1270,y=320)
#放置按钮来实现input_csv功能：
B3 = tk.Button(frame2,text='请选择match.csv文件',bg='blue',command=input_csv).place(anchor='w',x=1300,y=170)

#设定函数，让 line1 和 line2 能随着match的数据在x方向上平移：
match=[]
match_sp = []
def load_match():
    global line1
    global line2
    #根据filename3所制定的路径打开match文件并保存到列表match中，match是一个N*2的二维列表，每一行的第一个str表示sp的时间，第二个str表示tp的时间：
    with open(filename3,'r') as f:
        for line in f.readlines():
            match.append(line.strip('\n').split(','))
    for i in range(len(match)):
        match_sp.append(match[i][0])
    #每个画布canvas都有一套独立的坐标系，原点（0，0）在画布左上角，根据这里画布宽度的设定，左下角坐标为（0，300）
    #放置随match数据移动的竖线 line1 & line2,初始位置过点（0，0）和（0，300）：
    line1 = canvas1.create_line(0,0,0,390,width=1)
    line2 = canvas2.create_line(0,0,0,390,width=1)
    #根据match文件中sp音频的长度来设定滚动条S1的长度：
    S1.config(to=(float(match[-1][0])+1))
    
#设定函数，从Entry中读取数字值，来调整match时间点：
def set_match():
    if E1.get() != '':
         S1.set(E1.get()) 
         
        
#设定函数，用来获取scale的值并调整match时间点,1像素对应0.005s：
origin_scale = 0.00
def scale_selection(scale_var):
    global origin_scale
    offset = (var4.get() - origin_scale)//0.005
    canvas1.move(line1,offset,0)
    origin_scale = var4.get()
    moveline2()
    
#设定函数，可以用键盘上下左右键控制评估线的移动：
#0.005s对应1像素，所以0.1s对应20像素：
#上下键每次移动0.1s，左右键每次移动0.005s：
def moveline1(event):  # 绑定方向键
    global var4
    if event.keysym == "Up":
        canvas1.move(line1,20,0) # 移动的是 ID为line1的事物【move（2,0,-5）则移动ID为2的事物】，使得横坐标加0，纵坐标减5
        var4.set(var4.get()+0.1)
        moveline2()
    elif event.keysym == "Down":
        canvas1.move(line1,-20,0)
        var4.set(var4.get()-0.1)
        moveline2()
    elif event.keysym == "Left":            
        canvas1.move(line1,-1,0) 
        var4.set(var4.get()-0.005) 
        moveline2()          
    elif event.keysym == "Right":            
        canvas1.move(line1,1,0)
        var4.set(var4.get()+0.005) 
        moveline2()
#绑定方向键与函数
canvas1.bind_all("<KeyPress-Up>",moveline1) 
canvas1.bind_all("<KeyPress-Down>",moveline1)
canvas1.bind_all("<KeyPress-Left>",moveline1)
canvas1.bind_all("<KeyPress-Right>",moveline1)

#与match相关的Button
B4 = tk.Button(frame2,text='开始评估!',bg='blue',command=load_match).place(anchor='w',x=1300,y=210) 
B5 = tk.Button(frame2,text='手动设置时间点',bg='blue',command=set_match).place(anchor='w',x=1300,y=250) 
#canvas1.move(line1,1000,0)
#canvas2.move(line2,k,0)

#Entry1 用来手动键入match时间点：
E1 = tk.Entry(frame2,show=None,font=('Arial',18),text='请键入float数字时间点')     
#放置一个用来调节match时间点的Scale,digits代表现实的位数，variable绑定变量，移动scale将触发函数scale_selection：        
var4 = tk.DoubleVar()   
S1 = tk.Scale(frame2,from_=0.000,to=1000.000,digits=8,variable=var4,orient='vertical',resolution=0.005,command=scale_selection)

#根据line1的位置调整line2 match后的对应位置：
origin_tp_value = 0.00
def moveline2():
    global origin_tp_value 
#if var4.get() != 0:
    scale = var4.get()
    sp_index = binary_search(match_sp,scale)
    tp_value = float(match[sp_index][1])
    #0.005s对应1像素，所以1s对应200像素：
    offset = (tp_value - origin_tp_value)*200
    canvas2.move(line2,offset,0)
    origin_tp_value = tp_value
       
#将E1和S1的放置语句写到最后，避免出现NoneType Error:
E1.place(anchor='w',x=1270,y=390)  
S1.pack(side='right',fill='y')


"""
Happy Endding
"""
#放置logo在左上角：
#logo = Image.open('logo.png')
#
#logo = ImageTk.PhotoImage(logo.resize((25,25)))
#canvas_logo = tk.Canvas(window,width=55,height=55)
#image_logo = canvas_logo.create_image(20,20,image=logo)
#canvas_logo.pack(side='left',expand=False)

window.mainloop()

