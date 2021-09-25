# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 14:43:51 2021

@author: DELL
"""
import pymysql

db = pymysql.connect(host='localhost', user='root', password='XInyIw@20210707', port=3306, db='spiders')
cursor = db.cursor()
sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY (id))'
cursor.execute(sql)
db.close()