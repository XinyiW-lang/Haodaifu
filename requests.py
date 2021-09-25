# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 14:06:57 2021

@author: DELL
"""
import requests  

r = requests.get('https://www.baidu.com/')  
print(type(r))  
print(r.status_code)  
print(type(r.text))  
print(r.text)  
print(r.cookies)