# coding=GB2312
from urllib import request, parse
import json
from bs4 import BeautifulSoup
import os  #导入os模块
import sys
import io
import re
import time
import win32api
import win32con
import configparser



CookieIniFilePath = 'CookieConfig.ini'


#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
Connection = 'keep-alive'
Host = 'www.zict.cn'
global Cookies
global Identification
#Cookies = 'ASPSESSIONIDCQTDQDAC=ADLDPPHAMHDMCPGHKJDJAGOP; tmpCode=7240'
#验证码
Identification = ''
UserName = 'zywlssw'
UserPwd = 'zywlssw'
title_cod = 'login_win'



#获取get的response
def GetResponse(urlToGet,headers):

    req = request.Request(urlToGet, headers=headers)
    respone = request.urlopen(req)
    return respone




#获取cookie
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


#获取验证码
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


#登录
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
    # str = 'd登录'
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

#登录后确认
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
    # str = 'd登录'
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




#检测箱号输入是否合法
def CheckInputValid(boxid):
    boxid = boxid.strip()
    result = re.match('^[A-Z]{4}\d{7}$',boxid)
    if result:
        return True
    else:
        return False




#获取箱号的返回网页
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
    str = '查询'
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


# 获取箱号等信息
def GetBoxInfo(Boxid):
    if not CheckInputValid(Boxid):
        return None

    # 获取参数
    html = GetBoxHtml(Boxid)
    # 过滤无用信息，提取td开头的包含有效数据的str
    result = re.search('.*(<td>[A-Z]{4}\d{7}.*?)</tr>', html, re.S)
    # print(result)
    # print('result', result1.group(1))
    if result:
        # 去除<td>
        soup = BeautifulSoup(result.group(1), 'lxml')
        listRes = soup.find_all(name='td')
        DictRes = {
            '箱号': listRes[0].string.strip(),
            '提单号': listRes[1].string.strip(),
            '箱主': listRes[2].string.strip(),
            '箱型': listRes[3].string.strip(),
            '空重': listRes[4].string.strip(),
            '海关船名': listRes[5].string.strip(),
            '发送时间': listRes[6].string.strip(),
            '发送文件名': listRes[7].string.strip(),
            '回执': listRes[8].string.strip()}
        return DictRes
    else:
        NeedLogin = re.search('.*relogin.asp', html, re.S)
        setIniValid(False)
        print('检测失败')
        # if NeedLogin:
        #     win32api.MessageBox(0, "失去登录信息，尝试重新登录", "警告", win32con.MB_OK)
        return None

#保存cookies
def setIniCookies(cookiestmp):
    conf = configparser.ConfigParser()
    conf.read(CookieIniFilePath)
    conf.set('config', 'cookies', cookiestmp)
    with open(CookieIniFilePath, 'w') as fw:
        conf.write(fw)
#设置cookies是否有效
def setIniValid(isvalue):
    conf = configparser.ConfigParser()
    conf.read(CookieIniFilePath)
    conf.set('config', 'CookiesIsValid', str(isvalue))
    with open(CookieIniFilePath, 'w') as fw:
        conf.write(fw)

#设置cookies时间
def setIniTime():
    conf = configparser.ConfigParser()
    conf.read(CookieIniFilePath)
    conf.set('config', 'CookiesSettime', str(time.time()))
    with open(CookieIniFilePath, 'w') as fw:
        conf.write(fw)

#读取Cookies
def LoadCookie():
    conf = configparser.ConfigParser()
    conf.read(CookieIniFilePath)
    data = conf.get('config', 'cookies')
    return data

#检测cookies是否有效
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
#检测ini配置文件是否有效,是否有对应的配置项，如果没有，恢复默认项
def CheckIniFile():
    try:
        # setIniValid(str(True))
        conf = configparser.ConfigParser()
        conf.read(CookieIniFilePath)
        data = conf.get('config', 'CookiesIsValid')
        data = conf.get('config', 'CookiesSettime')
        data = conf.get('config', 'cookies')
    except:
        # 加载现有配置文件
        conf = configparser.ConfigParser()
        # 写入配置文件
        conf.add_section('config')  # 添加section
        # 添加值
        conf.set('config', 'CookiesIsValid', 'False')
        conf.set('config', 'CookiesSettime', '0')
        conf.set('config', 'cookies', 'ASPSESSIONIDAQTBRBCD=LPPPAHKBIMIKLALKBHICLKHD; tmpCode=4915')
        # 写入文件
        with open(CookieIniFilePath, 'w') as fw:
            conf.write(fw)


#设置cookies，如果cookies没有超时且有效，则不重新登录，否则，立即登录
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
    BoxIDfile = '箱号.txt'
    while True:
        os.system('cls')
        try :
            with open(BoxIDfile,'r+') as BoxFD:
                for BoxId in BoxFD:
                    if not CheckInputValid(BoxId):
                        print('箱号：' + BoxId.strip() + ' 箱号错误，请检查输入')
                        continue
                    SetCookies()
                    # BoxId = 'TRHU2604288'
                    Checkresult = GetBoxInfo(BoxId)
                    if Checkresult:
                        print('箱号：' + Checkresult['箱号'] + '  结果：' + Checkresult['回执'] + '时间：' + Checkresult['发送时间'])
                    else:
                        print('箱号：' + BoxId.strip() + '   结果： 未收到回执')

                    time.sleep(3)
        except:
            print('检查  ','\"',BoxIDfile,'\"  '+'是否存在，如果没有请新建文件'  )
        print('等待30s')
        time.sleep(30)




