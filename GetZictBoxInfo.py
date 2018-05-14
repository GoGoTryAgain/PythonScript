# coding=GB2312
from urllib import request, parse
from bs4 import BeautifulSoup
import os  #导入os模块
import sys  
import io  
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')  


url = 'http://www.zict.cn/svr_net/custom_exp_query.asp'

Cookie = 'td_cookie=18446744069669201114; ASPSESSIONIDAQSBTABC=JPAOKNFBOEDFGNEJILFGBNIL; td_cookie=18446744069607047567; ASPSESSIONIDCSSBTBBC=EDANJJCCLIDBLIJLOPOOHJBP; tmpCode=4682'






#获取箱号的返回网页
def GetBoxHtml(Boxid):
    headers = {
            'Host': 'www.zict.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.zict.cn/svr_net/custom_exp_query.asp',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': Cookie,
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin':'http://www.zict.cn',
            'Upgrade-Insecure-Requests': '1'
    }
    dict = {
    'ship_cod': '', 'ship_no': '', 'voyage': '', 'cntr_corp_cod': '', 'bill_no': '','cntr': Boxid
    }
    str = '查询'
    B1 = parse.quote(str.encode('GB2312'))
    data = parse.urlencode(dict)
    data = data + '&B1=' + B1
    data = bytes(data, encoding='GB2312')


    req = request.Request(url=url, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    html = response.read().decode('GB2312')
    #print(type(html))

    #print(soup.prettify())
    #print(html)
    return html

#检测箱号输入是否合法
def CheckInputValid(boxid):
    boxid = boxid.strip()
    result = re.match('^[A-Z]{4}\d{7}$',boxid)
    if result:
        return True
    else:
        return False
    
#获取箱号等信息    
def GetBoxInfo(Boxid):

    if not CheckInputValid(Boxid):
        return None
    
    #获取参数    
    html = GetBoxHtml(Boxid)
    #过滤无用信息，提取td开头的包含有效数据的str
    result = re.search('.*(<td>[A-Z]{4}\d{7}.*?)</tr>', html,re.S)
    #print(result)
    #print('result', result1.group(1))
    if result:
    #去除<td>
        soup = BeautifulSoup(result.group(1), 'lxml')
        listRes = soup.find_all(name='td')
        listCode = {
            '箱号': listRes[0].string.strip(),
            '提单号': listRes[1].string.strip(),
            '箱主': listRes[2].string.strip(),
            '箱型': listRes[3].string.strip(),
            '空重': listRes[4].string.strip(),
            '海关船名': listRes[5].string.strip(),
            '发送时间':listRes[6].string.strip(),
            '发送文件名': listRes[7].string.strip(),
            '回执': listRes[8].string.strip()}
        return listCode
        print(listCode)
    else:
        return None

            
print(GetBoxInfo('GLDU3865550'))



