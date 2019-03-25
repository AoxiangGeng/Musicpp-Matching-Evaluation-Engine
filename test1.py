#import tkinter as tk
#from PIL import ImageGrab, ImageTk
#master = tk.Toplevel()
#
#
#
#
##w.create_line(0, 0, 200, 100)
##w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
##
##w.create_rectangle(50, 25, 150, 75, fill="blue")
#img = ImageTk.PhotoImage(file='temp.png')
#label=tk.Label(master,image=img)
#label.mage=img
#screenWidth = master.winfo_screenwidth()
#screenHeight = master.winfo_screenheight()
#master.geometry(str(screenWidth)+'x'+str(screenHeight)+'+0+0')
#w = tk.Canvas(master, width=screenWidth, height=screenHeight)
#w.create_image(100,100,image=img)
#master.resizable(False,False)
#
#canvas = tk.Canvas(master,width=screenWidth,height=screenHeight)
#image = ImageTk.PhotoImage(ImageGrab.grab())
#canvas.create_image(screenWidth//2,screenHeight//2,image=image)
#def onMouseRightClick():
#    canvas.destroy()
#canvas.bind('<Enter>',onMouseRightClick)
#
#def onMouseMove(event):
#    global lastIm
#    global subIm
#    try:
#        w.delete(lastIm)
#    except:
#        pass
#    x = event.x+400
#    y = event.y
#    print(x,y)
#    subIm = ImageGrab.grab((x-200,y-10,x+100,y+200))
#    subIm = subIm.resize((600,400))
#    subIm = ImageTk.PhotoImage(subIm)
#    lastIm = w.create_image(event.x,event.y,anchor='center',image=subIm)
#    w.update()
#w.bind('<Motion>',onMouseMove)
#
#
#w.pack()
#master.mainloop()

import tkinter as tk 
from PIL import Image, ImageTk , ImageGrab

class LoadImage: 
    def __init__(self,root): 
     frame = tk.Frame(root) 
     self.canvas = tk.Canvas(frame,width=1500,height=1300) 
     self.canvas.pack() 
     frame.pack() 
     File = "temp.png" 
     self.orig_img = Image.open(File) 
     self.img = ImageTk.PhotoImage(self.orig_img,width=1500,height=1300) 
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

if __name__ == '__main__': 
    root = tk.Toplevel()
    root.geometry('1800x2000')
    cut = ImageGrab.grab()
    cut.save('cut.png')
    root.title("Crop Test") 
    App = LoadImage(root) 
    root.mainloop() 