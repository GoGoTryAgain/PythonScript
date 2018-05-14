# coding=GB2312
from urllib import request, parse
import requests
from bs4 import BeautifulSoup
import pytesser
import os  #导入os模块
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


folder_path = os.getcwd()  #设置图片要存放的文件目录
url = 'http://www.zict.cn/include/Code.asp'


def get_pic():
    print('开始网页get请求')
    resp = request(url)
    print('开始创建文件夹')
    mkdir(folder_path)  # 创建文件夹
    print('开始切换文件夹')
    os.chdir(folder_path)  # 切换路径至上面创建的文件夹
    name = 'Codeimg'
    file_name = name + '.jpg'
    print('开始保存图片')
    f = open(file_name, 'wb')
    f.write(resp.content)
    print(file_name, '图片保存成功！')
    f.close()

def mkdir(path):  ##这个函数创建文件夹
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        print('创建名字叫做', path, '的文件夹')
        os.makedirs(path)
        print('创建成功！')
    else:
        print(path, '文件夹已经存在了，不再创建')

get_pic()


