# coding=GB2312
from urllib import request, parse
import json
from bs4 import BeautifulSoup
import os  #����osģ��
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
Connection = 'keep-alive'
Host = 'www.zict.cn'
Cookies = 'ASPSESSIONIDCQTDQDAC=EMDDPPHAMBDFOADPCNGLADAL; tmpCode=2318'
#��֤��
Identification = ''
UserName = 'zywlssw'
UserPwd = 'zywlssw'
title_cod = 'login_win'



#��ȡget��response
def GetResponse(urlToGet,headers):

    req = request.Request(urlToGet, headers=headers)
    respone = request.urlopen(req)
    return respone


#��ȡcookie
def GetCookies():
    url = r'http://www.zict.cn/'
    headers = {
        'User-Agent': user_agent,
        'Connection':Connection ,
        'Host': Host
    }
    respone = GetResponse(url,headers)
    print(respone.getheaders())
    srcStr = respone.getheader('Set-Cookie')
    print(srcStr)
    cookies = re.match(r'^(.*);', srcStr).group(1)
    print(cookies)
    return cookies


#��ȡ��֤��
def GetIdentification():
    url = r'http://www.zict.cn/include/Code.asp'
    headers = {
        'User-Agent': user_agent,
        'Connection':Connection ,
        'Host': Host,
        'Cookie':Cookies,
    }
    respone = GetResponse(url,headers)
    print(respone.getheaders())
    srcStr = respone.getheader('Set-Cookie')
    print(srcStr)
    IdCode = re.match(r'^tmpCode=(.*);', srcStr).group(1)
    print(IdCode)
    return IdCode



def LoginZict():
    url = 'http://www.zict.cn/login.asp'
    headers = {
        'User-Agent': user_agent,
        'Connection':Connection ,
        'Host': Host,
        'Cookie':Cookies,
    }
    # str = 'd��¼'
    # Button = parse.quote(str.encode('GB2312'))
    Button = '%B5%C7%C2%BC'
    dict = {
    'Unam': UserName, 'uPwd': UserPwd, 'GCod': Identification, 'title_cod': title_cod
    }
    data = parse.urlencode(dict) + '&button=' + Button
    data = bytes(data, encoding='GB2312')
    print(data)
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    print(response.read())


def CheckLogin():
    url = 'http://www.zict.cn/login_info_chk.asp'
    headers = {
        'User-Agent': user_agent,
        'Connection':Connection ,
        'Host': Host,
        'Cookie':Cookies,
    }
    # str = 'd��¼'
    # Button = parse.quote(str.encode('GB2312'))
    dict = {
    'unam': UserName, 'upwd': UserPwd, 'gcod': Identification, 'title_cod': title_cod
    }
    data = parse.urlencode(dict)
    data = bytes(data, encoding='GB2312')
    print(data)
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    print(response.read())


#�����������Ƿ�Ϸ�
def CheckInputValid(boxid):
    boxid = boxid.strip()
    result = re.match('^[A-Z]{4}\d{7}$',boxid)
    if result:
        return True
    else:
        return False




#��ȡ��ŵķ�����ҳ
def GetBoxHtml(Boxid):
    url = 'http://www.zict.cn/svr_net/custom_exp_query.asp'
    headers = {
        'User-Agent': user_agent,
        'Connection': Connection,
        'Host': Host,
        'Cookie': Cookies,
    }
    dict = {
    'ship_cod': '', 'ship_no': '', 'voyage': '', 'cntr_corp_cod': '', 'bill_no': '','cntr': Boxid
    }
    str = '��ѯ'
    B1 = parse.quote(str.encode('GB2312'))
    data = parse.urlencode(dict)
    data = data + '&B1=' + B1
    data = bytes(data, encoding='GB2312')
    print(data)

    req = request.Request(url=url, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    html = response.read().decode('GB2312')
    #print(type(html))

    #print(soup.prettify())
    print(html)
    return html


# ��ȡ��ŵ���Ϣ
def GetBoxInfo(Boxid):
    if not CheckInputValid(Boxid):
        return None

    # ��ȡ����
    html = GetBoxHtml(Boxid)
    # ����������Ϣ����ȡtd��ͷ�İ�����Ч���ݵ�str
    result = re.search('.*(<td>[A-Z]{4}\d{7}.*?)</tr>', html, re.S)
    # print(result)
    # print('result', result1.group(1))
    if result:
        # ȥ��<td>
        soup = BeautifulSoup(result.group(1), 'lxml')
        listRes = soup.find_all(name='td')
        listCode = {
            '���': listRes[0].string.strip(),
            '�ᵥ��': listRes[1].string.strip(),
            '����': listRes[2].string.strip(),
            '����': listRes[3].string.strip(),
            '����': listRes[4].string.strip(),
            '���ش���': listRes[5].string.strip(),
            '����ʱ��': listRes[6].string.strip(),
            '�����ļ���': listRes[7].string.strip(),
            '��ִ': listRes[8].string.strip()}
        return listCode
        print(listCode)
    else:
        return None


Cookies = GetCookies()
Identification = GetIdentification()
Cookies = Cookies + '; tmpCode=' + Identification
LoginZict()
CheckLogin()
print(GetBoxInfo('OOLU1286663'))


