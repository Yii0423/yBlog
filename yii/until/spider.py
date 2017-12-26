import json
import re
import time
from html.parser import HTMLParser

import requests
from bs4 import BeautifulSoup

from yii.models import Essay

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/61.0.3163.100 Safari/537.36'}

proxies = {}


# 获取代理IP集合
def getProxies():
    ips = BeautifulSoup(requests.get('http://www.xicidaili.com/nn/1', headers=headers).text, 'html.parser').select("td")
    _ip = ''
    for ip in ips:
        if ips.index(ip) % 10 == 1:
            _ip += str(ip).replace('<td>', '').replace('</td>', '')
        if ips.index(ip) % 10 == 2:
            _ip += ':' + str(ip).replace('<td>', '').replace('</td>', '')
        if ips.index(ip) % 10 == 5:
            proxies[str(ip).replace('<td>', '').replace('</td>', '')] = _ip
            break


# 定义装饰器,在开始采集的第一步执行获取代理ip操作
def getIp(func):
    def deal():
        getProxies()
        func()

    return deal


# 今日头条(随笔-门户新闻)
def getJRTTNews():
    resultJRTT = []
    urlJRTT = 'https://www.toutiao.com/api/pc/feed/?category=internet&utm_source=toutiao&widen=1&max_behot_time=0' \
              '&max_behot_time_tmp=0&tadrequire=true&as=A1952AC482838EA&cp=5A4233B88E2A9E1' \
              '&_signature=2U4VlgAAgxNcsr.N.9i64NlOFY'
    bsJRTT = BeautifulSoup(requests.get(urlJRTT, headers=headers).content, 'html.parser')
    listJRTT = list(json.loads(str(bsJRTT))['data'])
    for news in listJRTT:
        labels = ''
        if 'label' in news:
            labels = ','.join(news['label'])
        try:
            objJRTT = Essay()
            objJRTT.categoryid = 2
            objJRTT.typeid = 13
            objJRTT.spiderid = news['group_id']
            objJRTT.seotitle = news['title']
            objJRTT.seokeywords = labels
            objJRTT.seodescription = news['abstract']
            objJRTT.sources = '今日头条'
            objJRTT.imagesurl = news['middle_image']
            objJRTT.filesurl = ''
            objJRTT.sort = int(round(time.time()))
            objJRTT.remarks = getJRTTNewsDetail('https://www.toutiao.com' + news['source_url'])
            resultJRTT.append(objJRTT)
        except BaseException as ex:
            pass
    return resultJRTT


# 今日头条新闻详情
def getJRTTNewsDetail(url):
    bsJRTTDetails = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    return HTMLParser().unescape(
        re.findall(r"content: '.*?'", str(bsJRTTDetails.contents[1]))[0].replace('content: \'', '').rstrip('\'')) \
           + "<p><a target=\"_blank\" href=\"" + url + "\"><span><small>* 转载自今日头条，点击跳转至原文链接</small>" \
                                                       "</span></a></p> "


# 网易新闻(随笔-门户新闻)
@getIp
def getWYXWNews():
    return ''


# 腾讯新闻(随笔-门户新闻)
@getIp
def getTXXWNews():
    return ''


# 百度新闻(随笔-门户新闻)
@getIp
def getBDXWNews():
    return ''
