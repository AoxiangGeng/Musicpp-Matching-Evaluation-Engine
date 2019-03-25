
from tkinter import *
 
root = Tk()
bfg = Button(root, text='change foreground', fg='red')
bfg.pack()
 
bbg = Button(root, text='change backgroud', bg='blue')
bbg.pack()
 
'''8.设置Button的边框
bd(bordwidth):缺省为1或2个像素
'''
# 创建5个Button边框宽度依次为：0，2，4，6，8
for b in [0, 1, 7, 13, 4]:
    Button(root,
           text=str(b),
           bd=b).pack()
'''9.设置Button的风格
relief/raised/sunken/groove/ridge
'''
for r in ['raised','sunken','groove','ridge']:
    Button(root,
    text = r,
    relief = r,
    width = 30).pack()
 

root.mainloop()