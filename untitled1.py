# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 14:08:58 2021

@author: DELL
"""
import re
import pandas as pd
import urllib.request
import time
#模拟浏览器
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
#获取网页数据
pat1 = '<a class="d-c-i-c-n-click" href="//.*?">(.*?)</a></p>'
team_name = []    #空列表存储团队名称
for j in range(1,20):
    try:
        url = "https://www.haodf.com/doctorteam/p_" + str(j) + ".htm"  #构造URL链接
        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req, timeout=500).read()
        str1 = data.decode("gbk")
        a1 = re.compile(pat1, re.S).findall(str1)
        team_name.extend(a1)
        print("第" + str(j) + "次成功")
        if j%10 == 0:
            time.sleep(10)
    except Exception as e:
        print("第" + str(j) + "次失败:", e)
print(team_name)
data_save = pd.DataFrame(team_name)
data_save.to_excel("team_save.xlsx",index=False,header=False)