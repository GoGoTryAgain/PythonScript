# coding=GB2312
from urllib import request, parse
import requests
from bs4 import BeautifulSoup
import pytesser
import os  #����osģ��
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


folder_path = os.getcwd()  #����ͼƬҪ��ŵ��ļ�Ŀ¼
url = 'http://www.zict.cn/include/Code.asp'


def get_pic():
    print('��ʼ��ҳget����')
    resp = request(url)
    print('��ʼ�����ļ���')
    mkdir(folder_path)  # �����ļ���
    print('��ʼ�л��ļ���')
    os.chdir(folder_path)  # �л�·�������洴�����ļ���
    name = 'Codeimg'
    file_name = name + '.jpg'
    print('��ʼ����ͼƬ')
    f = open(file_name, 'wb')
    f.write(resp.content)
    print(file_name, 'ͼƬ����ɹ���')
    f.close()

def mkdir(path):  ##������������ļ���
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        print('�������ֽ���', path, '���ļ���')
        os.makedirs(path)
        print('�����ɹ���')
    else:
        print(path, '�ļ����Ѿ������ˣ����ٴ���')

get_pic()


