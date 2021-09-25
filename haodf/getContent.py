# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 16:37:06 2021

@author: DELL
"""
import requests  
#import re
import time
from bs4 import BeautifulSoup
import csv
import json

BASE_URL_tnb = "https://www.haodf.com/jibing/tangniaobing/daifu_all_all_all_all_all_all_"
BASE_URL_byby = "https://www.haodf.com/jibing/buyunbuyu/daifu_all_all_all_all_all_all_"
BASE_URL_fy = "https://www.haodf.com/jibing/feiyan/daifu_all_all_all_all_all_all_"
BASE_URL_qx = "https://www.haodf.com/jibing/qixiong/daifu_all_all_all_all_all_all_"
BASE_URL_gxb = "https://www.haodf.com/jibing/guanxinbing/daifu_all_all_all_all_all_all_"

#regular expression for the links to experts
#pattern = re.compile(r'<a target="_blank" href="https?://[^\s]+" class="personweb-sickness-btn">个人网站</a>')

#get the html of one page
def get_one_page(url):  
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    response = requests.get(url, headers=headers)  
    if response.status_code == 200:  
        return response.text  
    return None  

#get all doctors' urls on that page
def get_urls_in_one_page(html):
    '''
    #滤出所有含“个人网站”字样的板块
    infos = re.findall(pattern, html)
    '''
    soup = BeautifulSoup(html, 'html.parser')
    
    #tags = soup.find_all('a', "personweb-sickness-btn")
    tags = soup.find_all('a', 'blue_a3')
    
    urls = set()
    for i in range(len(tags)):
        urls.add(tags[i]['href'])
    '''
    urls = set()
    for i in range(len(tags)):
        urls.add(tags[i].href)
        
    other_form = soup.find_all('a', 'blue_a3')
    for j in range(len(other_form)):
        urls.add(other_form[j].href)
    '''
    
    print("Num of doctors: " + str(len(urls)))
    
    '''
    string = ""
    #filter out all the doctors' personal links
    urls = re.findall(r'(https?://[^\s]+.html)',string.join(infos))
    '''
    return urls

#Get htmls of all doctors based on the url of their personal page, and return a set
#in order to avoid duplicate
def get_docs_url(total_page, BASE_URL):
    #count = 0
    cur_page = 1
    all_urls = set()
    
    while cur_page <= total_page:
        html = get_one_page(BASE_URL + str(cur_page) + '.htm')
        page_urls = get_urls_in_one_page(html)
        
        all_urls.update(page_urls)
        #count += len(page_urls)
        #防止网站封ip
        if cur_page%10 == 0:
            time.sleep(10)
            
        print("Currently at Page " + str(cur_page))
        
        cur_page += 1
    return all_urls

#爬取医生个人信息，写入csv文件
def get_info(writer,url,expert):
    
    temp_htm = get_one_page(url)
    
    if temp_htm is not None:
        soup = BeautifulSoup(get_one_page(url), 'html.parser')
    
        name = "NA"
        strength = "NA"
        #temp_nam and temp+strength might be NONETYPE
        temp_name = soup.find('h1', "doctor-name")
        temp_strength = soup.find('p','content')
        if temp_name is not None:
            name = temp_name.string
        if temp_strength is not None:
            strength = temp_strength.get_text(separator=" ").strip()
    
        intro = "NA"
        all_intro = soup.find_all('p','init-content')
        all_subtitle = soup.find_all('h3','introwarp-title')

        
        #简介
        if len(all_intro) > 0:
            intro = all_intro[0].get_text(separator=" ").strip()
            #print(name)
            #print(intro)
            #print()
        
        renzhi = "NA"
        keyan = "NA"
        rongyu = "NA"
        qita = "NA"
        
        #取细节信息， 如科研成果等
        if len(all_subtitle) > 0 :
            for i in range(len(all_subtitle)):
                if (all_subtitle[i].string == "社会任职"):
                    renzhi = all_intro[i+1].get_text(separator=" ").strip()
                    #print('renzhi: ' + renzhi)
                elif (all_subtitle[i].string == "科研成果" ):
                    keyan = all_intro[i+1].get_text(separator=" ").strip()
                    #print('keyan: ' + keyan)
                elif (all_subtitle[i].string == "获奖荣誉"):
                    rongyu = all_intro[i+1].get_text(separator=" ").strip()
                    #print('rongyu: ' + rongyu)
                else:
                    qita += all_intro[i+1].get_text(separator=" ").strip()
                    #print('qita: ' + qita)
                    
                        
                    
            #for i in range(len(all_intro)):
                #intro += all_intro[i].get_text(separator=" ").strip()
    
    
        writer.writerow({'name' : json.dumps(name, ensure_ascii=False),
                         'illness' : json.dumps(expert, ensure_ascii=False),
                         'shanchang' : json.dumps(strength, ensure_ascii=False),
                         'jianjie' : json.dumps(intro, ensure_ascii=False),
                         'renzhi' : json.dumps(renzhi, ensure_ascii=False),
                         'keyan' : json.dumps(keyan, ensure_ascii=False),
                         'rongyu' : json.dumps(rongyu, ensure_ascii=False),
                         'qita' : json.dumps(qita, ensure_ascii=False)})
    '''
    writer.writerow({'name' : name,
                     'expertise' : expert,
                     'good_at' : strength,
                     'brief_intro' : intro})
    '''
    
    
def main(): 
    '''
    urls = get_urls_in_one_page(get_one_page('https://www.haodf.com/jibing/tangniaobing/daifu_all_all_all_all_all_all_35.htm'))
    print(len(urls))
    #print(urls)
    '''
    # w:覆盖重写； a： 接着写
    with open('info_plus.csv', 'a', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['name', 'illness', 'shanchang', 'jianjie', 'renzhi', 'keyan', 'rongyu', 'qita']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
      
        '''
        #糖尿病
        all_urls_tnb = get_docs_url(67, BASE_URL_tnb)
        for u in all_urls_tnb:
            get_info(writer, u, '糖尿病')
        
        '''
        #不孕不育
        all_urls_byby = get_docs_url(67, BASE_URL_byby)
        for v in all_urls_byby:
            get_info(writer, v, '不孕不育')
        
        
        #肺炎
        all_urls_fy = get_docs_url(67, BASE_URL_fy)
        for w in all_urls_fy:
            get_info(writer, w, '肺炎')
     
        
        #气胸
        all_urls_qx = get_docs_url(67, BASE_URL_qx)
        for x in all_urls_qx:
            get_info(writer, x, '气胸')
        #冠心病
        all_urls_gxb = get_docs_url(67, BASE_URL_gxb)
        for y in all_urls_gxb:
            get_info(writer, y, '冠心病')
        
        

if __name__ == "__main__":
    main()