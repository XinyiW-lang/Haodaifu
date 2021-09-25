# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 15:52:16 2021

@author: DELL
"""
import urllib.request
import re
import random
uapools=[
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
]
ippools=[
    '1183.129.207.80:12520',
    '115.218.212.239:9000',
    '121.232.194.111:9999',
    '117.91.254.235:9999',
    '118.24.156.214:8118',
]
def ip(uapools,ippools):
    thisheaders=random.choice(uapools)
    print(thisheaders)
    thisip=random.choice(ippools)
    print(thisip)
    proxy = urllib.request.ProxyHandler({'http': thisip})
    opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    headers = ('User-Agent', thisheaders)
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)
 
try:
    for x in range(1,5):
        ip(uapools,ippools)
        print('当前为爬取第{}次。'.format(x))
        url='https://www.haodf.com/doctorteam/p_'+str(x)+'.htm'
        data=urllib.request.urlopen(url).read().decode('gbk','ignore')
        pat_url='<a class="d-c-i-c-n-click" href="(.*?)">'
        pat_title='">(.*?)</a></p>'
        alllink = re.compile(pat_url).findall(data)
        alltitle=re.compile(pat_title).findall(data)
        print(len(alllink))
        print(len(alltitle))
        for i in range(0,len(alllink),1):
            link = 'https:'+alllink[i]
            urllib.request.urlretrieve(link,"D:\\Python\\haodf\\data\\"+str(x)+str(i)+".html")
except urllib.error.URLError as e:
    if hasattr(e,'code'):
        print(e.code)
    if hasattr(e,'reason'):
        print(e.reason)