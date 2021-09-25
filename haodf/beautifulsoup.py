# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 22:01:59 2021

@author: DELL
"""
from bs4 import BeautifulSoup
import getContent

url1 = 'https://www.haodf.com/doctor/29060.html'
url2 = 'https://www.haodf.com/doctor/3297.html'
url3 = 'https://www.haodf.com/doctor/4027624215.html'
url4 = 'https://www.haodf.com/doctor/116750.html'


soup1 = BeautifulSoup(getContent.get_one_page(url1), 'html.parser')
soup2 = BeautifulSoup(getContent.get_one_page(url2), 'html.parser')
soup3 = BeautifulSoup(getContent.get_one_page(url3), 'html.parser')
soup4 = BeautifulSoup(getContent.get_one_page(url4), 'html.parser')

print(soup1.find_all('h3','introwarp-title'))
print(soup2.find_all('h3','introwarp-title'))
print(soup3.find_all('h3','introwarp-title'))
print(soup4.find_all('h3','introwarp-title'))