# coding=GB2312
import os  #导入os模块
import sys  
import io  
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')  



import tkinter as tk
root = tk.Tk()
root.title("Listbox 测试。")
# 存放list的容器
list_frame = tk.Frame(root)
list_frame.pack(expand=tk.YES, side=tk.TOP)
#存放按钮文本框的容器
button_frame = tk.Frame(root)
button_frame.pack(expand=tk.YES, side=tk.BOTTOM)
# 获取当前listbox中item值，并在控制台打印值
def print_item(event):
    items = lb.curselection()
    for k in items:
        print(lb.get(k))
var = tk.StringVar()#绑定listbox的列表值
var.set(('aa','bb','cc','dd','ee'))
lb = tk.Listbox(list_frame, listvariable = var, selectmode=tk.EXTENDED)#创建一个listbox
lb2 = tk.Listbox(list_frame, listvariable = var, selectmode=tk.EXTENDED)#创建一个listbox
lb.bind('<Button-1>',print_item)#绑定鼠标左键点击事件。
lb.pack(expand=tk.YES,side=tk.LEFT)
lb2.pack(expand=tk.YES,side=tk.LEFT)
# 添加listbox item的方法
def additem():
    lb.insert(tk.END,v.get())
    v.set('')
v = tk.StringVar()#绑定文本框的变量
en = tk.Entry(button_frame, textvariable = v).pack(side=tk.LEFT,expand=tk.YES)
b1 = tk.Button(button_frame, text="添加", command=additem).pack(side=tk.LEFT,expand=tk.YES)#添加一个item
b2 = tk.Button(button_frame, text="删除", command= lambda lb=lb:lb.delete(tk.ANCHOR)).pack(side=tk.LEFT,expand=tk.YES)#删除一个listbox中选中的item
root.mainloop()