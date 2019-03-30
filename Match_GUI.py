#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Header:
    
Music++ Matching Evaluation Engine

We developed a new multiple-spectrogram-alignment algorithms based on 
the Sonic Visualizer matching plugin. In order to evaluate the accuracy 
of this match results, an Evaluation Engine is built with the help of 
Tkinter.  The Matching algorithm will be uploaded separately.

@author: alex.Geng  brother.Nan
"""

import tkinter as tk
import pygame.mixer as mixer
import tkinter.filedialog
import tkinter.messagebox 
from  tkinter  import ttk
import app
from PIL import Image, ImageTk, ImageGrab 
import threading
import time
import cv2 
import os
import sys

"""
主体部分(Main Structure)
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
var1.set('请选择threshold和strength')
var2 = tk.StringVar()
var2.set('请选择threshold和strength')
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

    if distance1 < distance2:
        return array.index(array[height])
    elif distance2 <= distance1:
        return array.index(array[low])
    else:
        pass

#放置listbox，用于选择频谱图的threshold和darkness：
list1_1 = tk.StringVar()
list1_2 = tk.StringVar()
list2_1 = tk.StringVar()
list2_2 = tk.StringVar()
List1_1 = ttk.Combobox(frame1,textvariable=list1_1,width=5)
List1_2 = ttk.Combobox(frame1,textvariable=list1_2,width=5)
List2_1 = ttk.Combobox(frame2,textvariable=list2_1,width=5)   
List2_2 = ttk.Combobox(frame2,textvariable=list2_2,width=5)
#threshold: 0.1--1 根据能量值高低过滤多余音符
list1_items = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
#darkness: 0--9 频谱图深浅
list2_items = [0,1,2,3,4,5,6,7,8,9]
#赋值：
List1_1['values'] = list1_items
List2_1['values'] = list1_items
List1_2['values'] = list2_items
List2_2['values'] = list2_items
#默认为选择最后一个（threshold--1,darklness--9）:
List1_1.current(9)
List1_2.current(9)
List2_1.current(9)
List2_2.current(9)
#默认的threshold为1，darkness为9:
threshold1 = 1
darkness1 = 9
threshold2 = 1
darkness2 = 9
#绑定的下拉框值选择函数，*args表示可变参数：
def combox_select1_1(*args):
    global threshold1
    threshold1 = float(List1_1.get())
def combox_select1_2(*args):
    global darkness1
    darkness1 = int(List1_2.get())
def combox_select2_1(*args):
    global threshold2
    threshold2 = float(List2_1.get())
def combox_select2_2(*args):
    global darkness2
    darkness2 = int(List2_2.get())
#下拉框与相关函数的绑定：
List1_1.bind("<<ComboboxSelected>>",combox_select1_1)
List1_2.bind("<<ComboboxSelected>>",combox_select1_2)
List2_1.bind("<<ComboboxSelected>>",combox_select2_1)
List2_2.bind("<<ComboboxSelected>>",combox_select2_2)
#放置下拉框，threshold在左，darkness在右
List1_1.place(anchor='w',x=155,y=165)
List1_2.place(anchor='w',x=250,y=165)
List2_1.place(anchor='w',x=155,y=515)
List2_2.place(anchor='w',x=250,y=515)
"""    
#input函数用于导入音频文件,由用户选择文件，然后该函数获得文件的路径，将路径存储为filename1和filename2：
def input_wav1():
    global filename1
    filename1 = tk.filedialog.askdirectory()
    if filename1 != '':
        var1.set("文件加载成功")
    else:
        var1.set("您没有选择任何文件")
def input_wav2():
    global filename2
    filename2 = tk.filedialog.askdirectory()
    if filename2 != '':
        var2.set("文件加载成功")
    else:
        var2.set("您没有选择任何文件")

#两个Button用于导入音频文件：       
B1 = tk.Button(frame1,text='请选择sp_wav文件',command=input_wav1).place(anchor='w',x=200,y=170)
B2 = tk.Button(frame2,text='请选择tp_wav文件',command=input_wav2).place(anchor='w',x=200,y=520)
"""

"""
Zoom
"""
#I hope u will never use this function. Just in case you have a very poor eyesight.
class LoadImage(): 
    def __init__(self,root): 
     frame = tk.Frame(root) 
     self.canvas = tk.Canvas(frame,width=1800,height=2000,scrollregion=(0,0,3500,2000)) 
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
    #使用tk.Toplevel而不是tk.Tk,将可以避免出现canvas中的图像不显示的问题：
    root = tk.Toplevel()
    root.geometry('1800x1000')
    cut = ImageGrab.grab()
    cut.save('cut.png')
    root.title("Crop Test") 
    LoadImage(root)
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
设置音频播放(Mp3 Player)
"""
#初始化播放环境：
mixer.init()
#设定time_sp & time_tp的初始值，确保单独播放sp.wav或者tp.wav时不会报错
time_sp = 0.00
time_tp = 0.00
OFFSET1 = 0.00
OFFSET2 = 0.00
#设定定时器,用于实现tkinter的动态更新，只要开始播放音频文件，就会每隔0.01秒获取一次音频的播放时间点（这一句要考！）：
is_sp_play = False
def fun_timer1():
    global time_sp
    global time_tp
    global is_sp_play
    global OFFSET1
    #获取音频的播放时间信息， time_sp单位为秒
    #get_pos()----This gets the number of milliseconds that the music has
    #been playing for. The returned time only represents how long the music
    #has been playing; it does not take into account any starting 
    #position offsets. 
    time_sp = mixer.music.get_pos()/1000 + OFFSET1
    sp_index = binary_search(match_sp,time_sp)
    time_tp = float(match1[sp_index][1])
    #根据sp时间调整scale位置：
    S1.set(time_sp)
    S2.set(time_tp)
    #调整频谱图位置：
    scale_selection1()
    scale_selection2()
    global timer1
    #每隔0.1s执行一次线程：
    if is_sp_play:
        timer1 = threading.Timer(0.1, fun_timer1)
        timer1.start()
    else:
        time.sleep(0.1)
        timer1.cancel()
        
#用于sp的 播放，停止，暂停三个函数：
def track_start1():
    global time_sp
    global timer1
    global is_sp_play
    is_sp_play = True
    mixer.music.load(filename3+'/sp.mp3')
    #播放：
    mixer.music.play(0)
    #启动定时器程序：
    timer1 = threading.Timer(0,fun_timer1)
    timer1.start()
        
def track_stop1():
    global timer1
    global time_sp
    global time_tp
    global is_sp_play
    global OFFSET1
    global OFFSET2
    OFFSET1 = 0.00
    OFFSET2 = 0.00
    #关闭音频播放：
    mixer.music.stop()
    #停止定时器功能：
    is_sp_play = False
#    time.sleep(0)
    timer1.cancel()
    #归零
    time_sp = 0.00
    time_tp = 0.00
    scale_selection1()
    scale_selection2()
    
pause1 = False
def track_pause1():
    global pause1
    global is_sp_play
    global timer1
    global origin_scale1
    if pause1 == False:
        mixer.music.pause()
        pause1 = True
        is_sp_play = False
        time.sleep(0)
        timer1.cancel()
    else:
        mixer.music.rewind()
        mixer.music.set_pos(time_sp)
        mixer.music.unpause()
        pause1 = False
        is_sp_play = True
        timer1 = threading.Timer(0.1, fun_timer1)
        timer1.start()

#pageup1和pagedown1函数控制canvas1画布进行前后翻动,N代表移动的像素值，1像素0.005s，20像素0.1s：
def pageup1(n):
    canvas1.xview(tk.SCROLL, n, tk.UNITS) 

def pagedown1(n):
    canvas1.xview(tk.SCROLL, -n, tk.UNITS)        

#sp命名为track1：
#track1 = mixer.music.load(filename1)
#用于sp的 播放，停止，暂停三个按钮：
start_button1 = tk.Button(frame1,command = track_start1,text = "Start/播放")
start_button1.place(anchor='w',x=200,y=190)
stop_button1 = tk.Button(frame1,command = track_stop1,text = "Stop/停止")
stop_button1.place(anchor='w',x=200,y=210)
pause_button1 = tk.Button(frame1,command = track_pause1,text = "Pause/Unpause")
pause_button1.place(anchor='w',x=200,y=230)

#设定定时器,用于实现tkinter的动态更新，只要开始播放音频文件，就会每隔0.01秒获取一次音频的播放时间点（这一句要考！）：
is_tp_play = False
def fun_timer2():
    global time_tp
    global time_sp
    global is_tp_play
    global OFFSET2
    #获取音频的播放时间信息， time_tp单位为秒
    time_tp = mixer.music.get_pos()/1000 +OFFSET2
    tp_index = binary_search(match_tp,time_tp)
    time_sp = float(match2[tp_index][1])
    #根据tp时间调整scale位置：
    S2.set(time_tp)
    S1.set(time_sp)
    #调整频谱图位置：
    scale_selection1()
    scale_selection2()
    global timer2
    #每隔0.1s执行一次线程：
    if is_tp_play:
        timer2 = threading.Timer(0.1, fun_timer2)
        timer2.start()
    else:
        time.sleep(0.1)
        timer2.cancel()
    
#用于tp的 播放，停止，暂停三个函数：
def track_start2():
    global time_tp
    global timer2
    global is_tp_play
    is_tp_play = True
    mixer.music.load(filename3+'/tp.mp3')
    #播放：
    mixer.music.play(0)
    #启动定时器程序：
    timer2 = threading.Timer(0,fun_timer2)
    timer2.start()
 
def track_stop2():
    global timer2
    global time_sp
    global time_tp
    global is_tp_play
    global OFFSET1
    global OFFSET2
    OFFSET1 = 0.00
    OFFSET2 = 0.00
    #关闭音频播放：
    mixer.music.stop()
    #停止定时器功能：
    is_tp_play = False
#    time.sleep(0)
    timer2.cancel()
    #归零
    time_sp = 0.00
    time_tp = 0.00
    scale_selection1()
    scale_selection2()

pause2 = False
def track_pause2():
    global pause2
    global is_tp_play
    global timer2
    global origin_scale2
    if pause2 == False:
        mixer.music.pause()
        pause2 = True
        is_tp_play = False
        time.sleep(0)
        timer2.cancel()
    else:
        mixer.music.rewind()
        mixer.music.set_pos(time_tp)
        mixer.music.unpause()
        pause2 = False
        is_tp_play = True
        timer2 = threading.Timer(0.1, fun_timer2)
        timer2.start()
        
#pageup2和pagedown2函数控制canvas2画布进行前后翻动，N代表移动的像素值，1像素0.005s，20像素0.1s：：
def pageup2(n):
    canvas2.xview(tk.SCROLL, n, tk.UNITS) 
def pagedown2(n):
    canvas2.xview(tk.SCROLL, -n, tk.UNITS)   
#tp命名为track2：
#track2 = mixer.music.load(filename2)
#用于tp的 播放，停止，暂停三个按钮：
start_button2 = tk.Button(frame2,command = track_start2,text = "Start/播放")
start_button2.place(anchor='w',x=200,y=540)
stop_button2 = tk.Button(frame2,command = track_stop2,text = "Stop/停止")
stop_button2.place(anchor='w',x=200,y=560)
pause_button2 = tk.Button(frame2,command = track_pause2,text = "Pause/Unpause")
pause_button2.place(anchor='w',x=200,y=580)

#switch函数用于sp与tp之间的播放切换：
#例如，播放sp时，按下sp的暂停键，然后按switch按钮，音频将从tp的对应位置开始播放
def switch():
    global OFFSET1
    global OFFSET2
    global is_sp_play
    global is_tp_play
    global pause1
    global pause2
    if pause1 == True:
        OFFSET2 = time_tp
        pause1 = False
        is_tp_play = True
        #重新load文件并播放，将会归零get_pos()的返回值，所以这里把time_tp的时间作为OFFSET2保存：
        mixer.music.load(filename3+'/tp.mp3')
        mixer.music.play(0,time_tp)
        #不要忘记重启计时器：
        timer2 = threading.Timer(0.1, fun_timer2)
        timer2.start()
    elif pause2 == True:
        OFFSET1 = time_sp
        pause2 = False
        is_sp_play = True
        mixer.music.load(filename3+'/sp.mp3')
        mixer.music.play(0,time_sp)
        timer1 = threading.Timer(0.1, fun_timer1)
        timer1.start()
    else:
        pass
        
#switch按钮用于sp与tp之间的播放切换：
switch_button = tk.Button(frame2,font=('Arial',18),width=7,height=2,command = switch,text = "切换",bg='green',fg='blue',relief='raised', bd=3)
switch_button.place(anchor='w',x=200,y=410)

#将空格键和暂停pause/unpause绑定：
def space(spc):
    if is_sp_play == True or pause1 == True:
        track_pause1()
    elif is_tp_play == True or pause2 == True:
        track_pause2()
    else:
        pass
    
window.bind_all('<space>',space)

"""
频谱图部分(Spectrogram)
"""

#sp频谱图画布 canvas1:
canvas1 = tk.Canvas(frame1,bg='gray',width=900,height=390,scrollregion=(0,0,20000,8000),xscrollincrement=1)
hbar1 = tk.Scrollbar(frame1,orient='horizontal',bd=0)
hbar1.config(command=canvas1.xview)
canvas1.config(xscrollcommand=hbar1.set)

#tp频谱图画布 canvas2:
canvas2 = tk.Canvas(frame2,bg='gray',width=900,height=390,scrollregion=(0,0,20000,8000),xscrollincrement=1)
hbar2 = tk.Scrollbar(frame2,orient='horizontal',bd=0)
hbar2.config(command=canvas2.xview)
canvas2.config(xscrollcommand=hbar2.set)

#放置两个CheckButton，让用户选择是否重新绘制频谱图，还是使用之前画好的图片：
CheckVar1 = tk.IntVar()
CheckVar2 = tk.IntVar()
Check1 = tk.Checkbutton(frame1,text='使用现有图片？',variable=CheckVar1,onvalue=1,offvalue=0,height=1,width=12)
Check2 = tk.Checkbutton(frame2,text='使用现有图片？',variable=CheckVar2,onvalue=1,offvalue=0,height=1,width=12)
#生成的频谱图将以默认的名字 img1&img2 保存在当前目录下：
img1 = 'sp.png'
img2 = 'tp.png'
#用于生成频谱图的函数
length1 = 0.0
length2 = 0.0
def generate_specgram1():
    #必须将PhotoImage指定的tempImage声明为全局变量，否则h函数中绘制的图片在canvas中将不会被显示，这是tkinter的一个坑！
    global img1
    global filename3
    global length1
    global names1
    #names1用来动态生成变量
    names1 = locals()
    if CheckVar1.get() == 0:
        #用户选择重新绘制：
        showpic = app.Draw_pic(filename3,img1)
        #threshold:0-1; darkness:0-9
        length1 = showpic.energypic(threshold1,darkness1)
    else:
        #用户选择使用现有图片：
        temp = cv2.imread(filename3+"/"+img1)
        temp = temp.shape
        length1 = temp[1]
    #根据频谱图的长度调整canvas的窗口长度
    canvas1.config(scrollregion=(0,0,length1,length1))
    tempImage = cv2.imread(filename3+"/"+img1)
    #判断图片的长度是否超过30000像素，因为tk.PhotoImage最大只能导入30000x30000像素的图片：
    #所以如果图片的尺寸超过了30000像素，就将其截开，然后分别导入canvas拼接成完整的频谱图：
    n = length1//30000
    for i in range(n+1):
        if (i+1)*30000 < length1:
            #使用openCV对图片进行截取：
            cropImg = tempImage[:,i*30000:(i+1)*30000,:]
            #将截取的片段保存为temp.png，后面保存的png会覆盖之前的，因此不会占用太多空间
            cv2.imwrite(filename3+'/temp.png',cropImg)
            #读取截取片段并用tk.PhotoImage实例化，变量名为names['tempImagei']，i随着for循环递增,并且已被声明为全局变量：
            names1['tempImage'+str(i)]=tk.PhotoImage(file = filename3+'/temp.png')
            canvas1.create_image(450+i*30000,194,anchor='w',image=names1['tempImage'+str(i)])
        else:
            #最后一个片段只需要截到length1，而不是(i+1)*30000:
            cropImg = tempImage[:,i*30000:length1,:]
            cv2.imwrite(filename3+'/temp.png',cropImg)
            names1['tempImage'+str(i)] = tk.PhotoImage(file = filename3+'/temp.png')
            canvas1.create_image(450+i*30000,194,anchor='w',image=names1['tempImage'+str(i)])
                    
def generate_specgram2():
    global img2
    global filename3
    #必须将PhotoImage指定的tempImage声明为全局变量，否则图片在canvas中将不会被显示
    global length2
    global names2
    names2 = locals()
    if CheckVar2.get() == 0:
        #用户选择重新绘制：
        showpic = app.Draw_pic(filename3,img2)
        #threshold:0-1; darkness:0-9
        length2 = showpic.energypic(threshold2,darkness2)
    else:
        #用户选择使用现有图片：
        temp = cv2.imread(filename3+"/"+img2)
        temp = temp.shape
        length2 = temp[1]
    #根据频谱图的长度调整canvas的窗口长度
    canvas2.config(scrollregion=(0,0,length2,length2))  
    tempImage = cv2.imread(filename3+"/"+img2)
    #判断图片的长度是否超过30000像素：
    n = length2//30000
    for j in range(n+1):
        if (j+1)*30000 < length2:
            cropImg = tempImage[:,j*30000:(j+1)*30000,:]
            cv2.imwrite(filename3+'/temp.png',cropImg)
            names2['tempImage'+str(j)]=tk.PhotoImage(file = filename3+'/temp.png')
            canvas2.create_image(450+j*30000,194,anchor='w',image=names2['tempImage'+str(j)])
        else:
            cropImg = tempImage[:,j*30000:length2,:]
            cv2.imwrite(filename3+'/temp.png',cropImg)
            names2['tempImage'+str(j)] = tk.PhotoImage(file = filename3+'/temp.png')
            canvas2.create_image(450+j*30000,194,anchor='w',image=names2['tempImage'+str(j)])
                    
                
    
#用于生成频谱图的两个按钮：
B_sp = tk.Button(frame1,text = "绘制SP频谱图",command=generate_specgram1)
B_tp = tk.Button(frame2,text = "绘制TP频谱图",command=generate_specgram2)
B_sp.place(anchor='w',x=250,y=250)
B_tp.place(anchor='w',x=250,y=600)
Check1.place(anchor='w',x=130,y=250)
Check2.place(anchor='w',x=130,y=600)
"""
Match部分
"""

#match和音频文件的默认地址：
filename3 = '/Users/alex/Desktop/work/Test_madmom/match_test_data/test/GUI/tschaikovsky_cut1'

var3 = tk.StringVar()
var3.set('请选择match文件夹')
#导入match数据：
def input_csv():
    global filename3
    filename3 = tk.filedialog.askdirectory()
    if filename3 != '':
        var3.set("文件加载成功")
        print('\n文件地址:\n'+filename3)
    else:
        var3.set("您没有选择任何文件")
        
#提示导入match文件并显示其路径：        
L4 = tk.Label(frame2, textvariable=var3,bg='blue',fg='white',font=('Arial',10),width=35,height=5).place(anchor='w',x=1270,y=460)
#放置按钮来实现input_csv功能：
B3 = tk.Button(frame2,text='请选择match文件',bg='blue',command=input_csv).place(anchor='w',x=1300,y=170)

#设定函数，让 line1 和 line2 能随着match的数据在x方向上平移：
match1=[]
match2 = []
match_sp = []
match_tp = []

def load_match():
    global line1
    global line2
    global canvas3
    #根据filename3所制定的路径打开match文件并保存到列表match中，match是一个N*2的二维列表，每一行的第一个str表示sp的时间，第二个str表示tp的时间：
    #match1对应sp在前的文件，match2对应tp在前的文件：
    with open(filename3+'/match.csv','r') as f:
        for line in f.readlines():
            match1.append(line.strip('\n').split(','))
    with open(filename3+'/match_reverse.csv','r') as g:
        for line in g.readlines():
            match2.append(line.strip('\n').split(','))
    #将sp，tp的时间点分别保存为一维list，方便之后进行binary search：
    for i in range(len(match1)):
        match_sp.append(match1[i][0])
    for j in range(len(match2)):
        match_tp.append(match2[j][0])
    #每个画布canvas都有一套独立的坐标系，原点（0，0）在画布左上角，根据这里画布宽度的设定，左下角坐标为（0，300）
    #当按下‘开始评估’键时，将在画布正中间生成一条竖线，位置固定,其位置与频谱图的初始位置重合：
    canvas3 = tk.Canvas(frame1,width=1,height=740,bg='black').place(anchor='w',x=800,y=512)
    #根据match文件中音频的长度来设定滚动条S1,S2的长度：
    S1.config(to=(float(match1[-1][0])+1))
    S2.config(to=(float(match2[-1][0])+1))

#设定函数，从Entry中读取数字值，来调整scale时间点：
def set_match1():
    global time_sp
    global time_tp
    global OFFSET1
    if E1.get() != '':
         S1.set(E1.get())
         OFFSET1 += float(E1.get()) - time_sp
         time_sp = float(E1.get())
         sp_index = binary_search(match_sp,time_sp)
         time_tp = float(match1[sp_index][1])
         scale_selection1()
         scale_selection2()

def set_match2():
    global time_tp
    global time_sp
    global OFFSET2
    if E2.get() != '':
         S2.set(E2.get()) 
         OFFSET2 += float(E2.get()) - time_tp
         time_tp = float(E2.get())
         tp_index = binary_search(match_tp,time_tp)
         time_sp = float(match2[tp_index][1])
         scale_selection1()
         scale_selection2()
         
#该函数用于判断数字num是否在lis【0】--lis【1】的范围内
def within(num,lis):
    if lis[0] <= num and lis[1] >= num:
        return True
    else:
        return False        

#定义函数set_scale用于拖动进度条来选择音频播放位置：
def set_scale1(scale1):
    global time_sp
    global time_tp
    global OFFSET1
    if pause1 == True:
        OFFSET1 += float(S1.get()) - time_sp
        time_sp = float(S1.get())
        sp_index = binary_search(match_sp,time_sp)
        time_tp = float(match1[sp_index][1])
        scale_selection1()
        scale_selection2()
    else:
        pass

def set_scale2(scale2):
    global time_sp
    global time_tp
    global OFFSET2
    if pause2 == True:
        OFFSET2 += float(S2.get()) - time_tp
        time_tp = float(S2.get())
        tp_index = binary_search(match_tp,time_tp)
        time_sp = float(match2[tp_index][1])
        scale_selection1()
        scale_selection2()
    else:
        pass
 
#设定函数，用来获取scale的值并调整match时间点,1像素对应0.005s：
origin_scale1 = 0.00
def scale_selection1():
    global origin_scale1
    global time_sp 
    global time_tp
    #根据sp时间调整频谱图位置：
    offset1 = round((time_sp - origin_scale1)*200)
    if offset1 > 0:
        pageup1(offset1)
    elif offset1 < 0:
        pagedown1(-offset1)
    origin_scale1 = time_sp
    
origin_scale2 = 0.00
def scale_selection2():
    global origin_scale2
    global time_tp 
    global time_sp
    #根据tp时间调整频谱图位置：
    offset2 = round((time_tp - origin_scale2)*200)
    #print(time_tp,origin_scale2,(time_tp-origin_scale2)*200,offset2)
    if offset2 > 0:
        pageup2(offset2)
    elif offset2 < 0:
        pagedown2(-offset2)
    origin_scale2 = time_tp
    
#设定函数，可以用键盘上下左右键控制评估线的移动：
#0.005s对应1像素，所以0.1s对应20像素：
#上下键每次移动0.5s，左右键每次移动0.005s：
def moveline(event):  # 绑定方向键
    global pause1
    global pause2
    global time_sp
    global time_tp
    global OFFSET1
    global OFFSET2
    if pause1 == True:
        if event.keysym == "Up":
            time_sp += 0.5
            OFFSET1 += 0.5
        elif event.keysym == "Down":
            time_sp -= 0.5
            OFFSET1 -= 0.5
        elif event.keysym == "Left":
            time_sp -= 0.05
            OFFSET1 -= 0.05
        elif event.keysym == "Right":
            time_sp += 0.05
            OFFSET1 += 0.05
        sp_index = binary_search(match_sp,time_sp)
        time_tp = float(match1[sp_index][1])
        scale_selection1()
        scale_selection2()

    elif pause2 == True:
        if event.keysym == "Up":
            time_tp += 0.5
            OFFSET2 += 0.5
        elif event.keysym == "Down":
            time_tp -= 0.5
            OFFSET2 -= 0.5
        elif event.keysym == "Left":
            time_tp -= 0.05
            OFFSET2 -= 0.05
        elif event.keysym == "Right":
            time_tp += 0.05
            OFFSET2 += 0.05
        tp_index = binary_search(match_tp,time_tp)
        time_sp = float(match2[tp_index][1])
        scale_selection1()
        scale_selection2()
    else:
        pass
    S1.set(time_sp)
    S2.set(time_tp)
    
#绑定方向键与函数
canvas1.bind_all("<KeyPress-Up>",moveline) 
canvas1.bind_all("<KeyPress-Down>",moveline)
canvas1.bind_all("<KeyPress-Left>",moveline)
canvas1.bind_all("<KeyPress-Right>",moveline)
canvas2.bind_all("<KeyPress-Up>",moveline) 
canvas2.bind_all("<KeyPress-Down>",moveline)
canvas2.bind_all("<KeyPress-Left>",moveline)
canvas2.bind_all("<KeyPress-Right>",moveline)
#与match相关的Button
B4 = tk.Button(frame2,text='开始评估!',bg='blue',command=load_match).place(anchor='w',x=1300,y=210) 
B5 = tk.Button(frame2,text='手动设置sp时间点',bg='blue',command=set_match1).place(anchor='w',x=1300,y=250) 
B6 = tk.Button(frame2,text='手动设置tp时间点',bg='blue',command=set_match2).place(anchor='w',x=1300,y=350) 

#Entry1,2 用来手动键入scale时间点：
E1 = tk.Entry(frame2,show=None,font=('Arial',18),text='请键入float数字时间点',width=15)
E2 = tk.Entry(frame2,show=None,font=('Arial',18),text='请键入float数字时间点',width=15)        
#放置一个用来调节match时间点的Scale,digits代表现实的位数，variable绑定变量，移动scale将触发函数scale_selection：        
var4 = tk.DoubleVar() 
var5 = tk.DoubleVar()   
S1 = tk.Scale(frame2,width=13,from_=0.000,to=1000.000,digits=8,variable=var4,orient='vertical',resolution=0.001,command=set_scale1)
S2 = tk.Scale(frame2,width=13,from_=0.000,to=1000.000,digits=8,variable=var5,orient='vertical',resolution=0.001,command=set_scale2)
       
#将E1,E2和S1,S2的放置语句写到最后，避免出现NoneType Error:
E1.place(anchor='w',x=1300,y=300)  
E2.place(anchor='w',x=1300,y=400) 
#放置scale1，2， 1在左2在右，1代表sp2代表tp：
S2.pack(side='right',fill='y')
S1.pack(side='right',fill='y')

"""
Happy Endding
"""

#显示开发者信息：
def info():
    tkinter.messagebox.showinfo(title='Developer Info', message='Develops:\n\n Alex.Geng\tEmail: gengaoxiang@musicpp.com\n\n Brother.Nan\tEmail: renzhennan@musicpp.com')  
B7 = tk.Button(frame2,text='显示开发者信息',bg='blue',command=info).place(anchor='w',x=1300,y=530)
#放置scrollbar-- hbar1 & hbar2至窗口底部，并铺满整个x轴:
hbar2.pack(side='bottom',fill='x')
hbar1.pack(side='bottom',fill='x')
#最后再放置canvas1&2， 防止出现NoneType has no attribute XXX Error:
canvas1.place(anchor='w',x=350,y=340)
canvas2.place(anchor='w',x=350,y=690)

#设置一个重启函数：
def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)
#放置重启按钮在开发者信息按钮下方：  
ButtonRestart = tk.Button(frame2,text='重启/Restart',command=restart_program,bg='blue').place(anchor='w',x=1300,y=600)

#放置logo：
Logo = tk.PhotoImage(file='logo.png')
canvas_logo = tk.Canvas(frame2,width=150,height=150)
canvas_logo.create_image(0,75,anchor='w',image=Logo)
canvas_logo.place(anchor='w',x=1300,y=750)

#定义打印时间函数：
def print_time():
    print('\nSP时间点为:   ',time_sp)
    print('\tTP时间点为:   ',time_tp)
#放置打印时间按钮：
B8 = tk.Button(frame2,text='打印时间信息',font=('Arial',18),width=14,height=2,bg='blue',command=print_time)
B8.place(anchor='w',x=165,y=750)

#start the mainloop:
window.mainloop()

