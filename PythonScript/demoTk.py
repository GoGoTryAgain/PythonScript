# coding=GB2312
import os  #����osģ��
import sys  
import io  
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')  



import tkinter as tk
root = tk.Tk()
root.title("Listbox ���ԡ�")
# ���list������
list_frame = tk.Frame(root)
list_frame.pack(expand=tk.YES, side=tk.TOP)
#��Ű�ť�ı��������
button_frame = tk.Frame(root)
button_frame.pack(expand=tk.YES, side=tk.BOTTOM)
# ��ȡ��ǰlistbox��itemֵ�����ڿ���̨��ӡֵ
def print_item(event):
    items = lb.curselection()
    for k in items:
        print(lb.get(k))
var = tk.StringVar()#��listbox���б�ֵ
var.set(('aa','bb','cc','dd','ee'))
lb = tk.Listbox(list_frame, listvariable = var, selectmode=tk.EXTENDED)#����һ��listbox
lb2 = tk.Listbox(list_frame, listvariable = var, selectmode=tk.EXTENDED)#����һ��listbox
lb.bind('<Button-1>',print_item)#������������¼���
lb.pack(expand=tk.YES,side=tk.LEFT)
lb2.pack(expand=tk.YES,side=tk.LEFT)
# ���listbox item�ķ���
def additem():
    lb.insert(tk.END,v.get())
    v.set('')
v = tk.StringVar()#���ı���ı���
en = tk.Entry(button_frame, textvariable = v).pack(side=tk.LEFT,expand=tk.YES)
b1 = tk.Button(button_frame, text="���", command=additem).pack(side=tk.LEFT,expand=tk.YES)#���һ��item
b2 = tk.Button(button_frame, text="ɾ��", command= lambda lb=lb:lb.delete(tk.ANCHOR)).pack(side=tk.LEFT,expand=tk.YES)#ɾ��һ��listbox��ѡ�е�item
root.mainloop()