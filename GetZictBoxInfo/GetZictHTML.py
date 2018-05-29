# coding=GB2312
from urllib import request, parse
import json
from bs4 import BeautifulSoup
import os  #����osģ��
import sys
import io
import re
import time
import configparser
import random


CookieIniFilePath = 'CookieConfig.ini'


#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
Connection = 'keep-alive'
Host = 'www.zict.cn'
global Cookies
global Identification
#Cookies = 'ASPSESSIONIDCQTDQDAC=ADLDPPHAMHDMCPGHKJDJAGOP; tmpCode=7240'
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
    global Cookies
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
    IdCode = re.match(r'^tmpCode=(\d{4});', srcStr).group(1)
    print(IdCode)
    return IdCode


#��¼
def LoginZict():
    global Cookies
    global Identification
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
    #print(data)
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    #print(response.read())

#��¼��ȷ��
def CheckLogin():
    global Cookies
    global Identification
    url = 'http://www.zict.cn/login_info_chk.asp'
    headers = {
        'User-Agent': user_agent,
        'Connection':Connection ,
        'Host': Host,
        'Cookie':Cookies,
        'Referer':'http://www.zict.cn/login.asp',
        'Content-Type':'application/x-www-form-urlencoded'

    }
    # str = 'd��¼'
    # Button = parse.quote(str.encode('GB2312'))
    dict = {
    'unam': UserName, 'upwd': UserPwd, 'gcod': Identification, 'title_cod': title_cod
    }
    data = parse.urlencode(dict)
    data = bytes(data, encoding='GB2312')
    #print(data)
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
    global Cookies
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
    #print(Cookies)
    str = '��ѯ'
    B1 = parse.quote(str.encode('GB2312'))
    data = parse.urlencode(dict)
    data = data + '&B1=' + B1
    data = bytes(data, encoding='GB2312')
    #print(data)

    req = request.Request(url=url, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    html = response.read().decode('GB2312')
    #print(soup.prettify())
    #print(html)
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
        DictRes = {
            '���': listRes[0].string.strip(),
            '�ᵥ��': listRes[1].string.strip(),
            '����': listRes[2].string.strip(),
            '����': listRes[3].string.strip(),
            '����': listRes[4].string.strip(),
            '���ش���': listRes[5].string.strip(),
            '����ʱ��': listRes[6].string.strip(),
            '�����ļ���': listRes[7].string.strip(),
            '��ִ': listRes[8].string.strip()}
        return DictRes
    else:
        NeedLogin = re.search('.*relogin.asp', html, re.S)
        setIniValid(False)
        print('���ʧ��')
        # if NeedLogin:
        #     win32api.MessageBox(0, "ʧȥ��¼��Ϣ���������µ�¼", "����", win32con.MB_OK)
        return None

#����cookies
def setIniCookies(cookiestmp):
    conf = configparser.ConfigParser()
    conf.read(CookieIniFilePath)
    conf.set('config', 'cookies', cookiestmp)
    with open(CookieIniFilePath, 'w') as fw:
        conf.write(fw)
#����cookies�Ƿ���Ч
def setIniValid(isvalue):
    conf = configparser.ConfigParser()
    conf.read(CookieIniFilePath)
    conf.set('config', 'CookiesIsValid', str(isvalue))
    with open(CookieIniFilePath, 'w') as fw:
        conf.write(fw)

#����cookiesʱ��
def setIniTime():
    conf = configparser.ConfigParser()
    conf.read(CookieIniFilePath)
    conf.set('config', 'CookiesSettime', str(time.time()))
    with open(CookieIniFilePath, 'w') as fw:
        conf.write(fw)

#��ȡCookies
def LoadCookie():
    conf = configparser.ConfigParser()
    conf.read(CookieIniFilePath)
    data = conf.get('config', 'cookies')
    return data

#���cookies�Ƿ���Ч
def checkcookies():
    conf = configparser.ConfigParser()
    conf.read(CookieIniFilePath)

    if conf.getboolean('config', 'CookiesIsValid'):
        timeBack = conf.getfloat('config', 'cookiessettime')
        timenow = time.time()
        timediff = timenow - float(timeBack)
        if timediff < 0 or timediff > 3600 * 3:
            return False
        else:
            return True
    else:
        return False
#���ini�����ļ��Ƿ���Ч,�Ƿ��ж�Ӧ����������û�У��ָ�Ĭ����
def CheckIniFile():
    try:
        # setIniValid(str(True))
        conf = configparser.ConfigParser()
        conf.read(CookieIniFilePath)
        data = conf.get('config', 'CookiesIsValid')
        data = conf.get('config', 'CookiesSettime')
        data = conf.get('config', 'cookies')
    except:
        # �������������ļ�
        conf = configparser.ConfigParser()
        # д�������ļ�
        conf.add_section('config')  # ���section
        # ���ֵ
        conf.set('config', 'CookiesIsValid', 'False')
        conf.set('config', 'CookiesSettime', '0')
        conf.set('config', 'cookies', 'ASPSESSIONIDAQTBRBCD=LPPPAHKBIMIKLALKBHICLKHD; tmpCode=4915')
        # д���ļ�
        with open(CookieIniFilePath, 'w') as fw:
            conf.write(fw)


#����cookies�����cookiesû�г�ʱ����Ч�������µ�¼������������¼
def SetCookies():
    global  Cookies
    global Identification
    CheckIniFile()
    if checkcookies():
        Cookies = LoadCookie()
    else:
        Cookies = LoadCookie()
        CookiesContext = GetCookies()
        Cookies = CookiesContext +'; tmpCode=1234'
        Identification = GetIdentification()
        Cookies = CookiesContext + '; tmpCode=' + Identification
        print('cookies is ' + Cookies)
        LoginZict()
        CheckLogin()
        setIniCookies(Cookies)
        setIniTime()
        setIniValid(True)


if __name__ == '__main__':
    BoxIDfile = '���.txt'
    while True:
        os.system('cls')
        linebox = 0
        try :
            with open(BoxIDfile,'r+') as BoxFD:
                for BoxId in BoxFD:
                    linebox = linebox + 1
                    if not CheckInputValid(BoxId):
                        if BoxId.strip().lstrip().rstrip('\n').rstrip('\r') == '':
                            continue
                        else:
                            print('��ţ�' + BoxId.strip() + '           ��ʽ������������,����λ�ڵ�' + str(linebox) + '��' )
                            continue
                    SetCookies()
                    Checkresult = GetBoxInfo(BoxId)
                    if Checkresult:
                        print('��ţ�' + Checkresult['���'] + '     �����' + Checkresult['��ִ'] + 'ʱ�䣺' + Checkresult['����ʱ��'])
                    else:
                        print('��ţ�' + BoxId.strip() + '   ����� δ�յ���ִ')

                    time.sleep(random.uniform(1,2.5))
        except IOError:
            print('���  ','\"',BoxIDfile,'\"  '+'�Ƿ���ڣ����û�����½��ļ�'  )
            exit()
            os.system('cmd')
        except:
            print('��������'  )
            exit()
            os.system('cmd')


        timeWaitTotal = 30
        for timewait in range(timeWaitTotal):
            time.sleep(1)
            if not timewait % 5:
                print(timeWaitTotal - timewait,'s�����»�ȡ')





