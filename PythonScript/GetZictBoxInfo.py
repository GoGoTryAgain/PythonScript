# coding=GB2312
from urllib import request, parse
from bs4 import BeautifulSoup
import os  #����osģ��
import sys  
import io  
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')  


url = 'http://www.zict.cn/svr_net/custom_exp_query.asp'

Cookie = 'td_cookie=18446744069669201114; ASPSESSIONIDAQSBTABC=JPAOKNFBOEDFGNEJILFGBNIL; td_cookie=18446744069607047567; ASPSESSIONIDCSSBTBBC=EDANJJCCLIDBLIJLOPOOHJBP; tmpCode=4682'






#��ȡ��ŵķ�����ҳ
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
    str = '��ѯ'
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

#�����������Ƿ�Ϸ�
def CheckInputValid(boxid):
    boxid = boxid.strip()
    result = re.match('^[A-Z]{4}\d{7}$',boxid)
    if result:
        return True
    else:
        return False
    
#��ȡ��ŵ���Ϣ    
def GetBoxInfo(Boxid):

    if not CheckInputValid(Boxid):
        return None
    
    #��ȡ����    
    html = GetBoxHtml(Boxid)
    #����������Ϣ����ȡtd��ͷ�İ�����Ч���ݵ�str
    result = re.search('.*(<td>[A-Z]{4}\d{7}.*?)</tr>', html,re.S)
    #print(result)
    #print('result', result1.group(1))
    if result:
    #ȥ��<td>
        soup = BeautifulSoup(result.group(1), 'lxml')
        listRes = soup.find_all(name='td')
        listCode = {
            '���': listRes[0].string.strip(),
            '�ᵥ��': listRes[1].string.strip(),
            '����': listRes[2].string.strip(),
            '����': listRes[3].string.strip(),
            '����': listRes[4].string.strip(),
            '���ش���': listRes[5].string.strip(),
            '����ʱ��':listRes[6].string.strip(),
            '�����ļ���': listRes[7].string.strip(),
            '��ִ': listRes[8].string.strip()}
        return listCode
        print(listCode)
    else:
        return None

            
print(GetBoxInfo('GLDU3865550'))



