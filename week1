#!/usr/bin/env python
# coding: utf-8

# In[18]:


from bs4 import BeautifulSoup
import requests
import time

url='http://fhya8ff4798d0cae4ed0b725f57cfc9334c1sbpovbf6qwxvx6q9u.fbzz.libproxy.ruc.edu.cn/full_record.do?product=UA&search_mode=AdvancedSearch&qid=1&SID=8FshHtJS1ljw8QxR3z5&page=1&doc=1'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Cookie':'optimizelyEndUserId=oeu1590569202932r0.8946896902430339; _ga=GA1.3.146798051.1590569208; amplitude_id_408774472b1245a7df5814f20e7484d0ruc.edu.cn=eyJkZXZpY2VJZCI6IjFlMDc5MGEwLTU0ODAtNGZlZS05YzZmLTE4MmNhNTRiNGUwNyIsInVzZXJJZCI6bnVsbCwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNTkwODI4OTM2NDE5LCJsYXN0RXZlbnRUaW1lIjoxNTkwODI4OTk0OTg2LCJldmVudElkIjowLCJpZGVudGlmeUlkIjoxNCwic2VxdWVuY2VOdW1iZXIiOjE0fQ==; UM_distinctid=173802d4ae3165-0736d5966079da-b7a1334-100200-173802d4ae59e3; _hjid=e1af6047-dba4-45a5-9594-f502d155cea1; _hjAbsoluteSessionInProgress=1; CWJSESSIONID=CCD16235FDB21DE6FFE5CB03ACD5B6D6; cwsid=73383bd8558c4a16; _sp_ses.58cf=*; _sp_id.58cf=48248723-a40c-4ff8-97db-39100ccb3c6e.1597288425.6.1597769311.1597766247.7857d8f3-7cea-4a81-ae7a-fa6565b33e56'
}

def get_infos(url):
    wb_data=requests.get(url,headers=headers)
    time.sleep(4)
    soup=BeautifulSoup(wb_data.text,'lxml')
    titles=soup.find_all("div",class_='title')
    names=soup.find_all("p",class_="FR_field")
    abstracts=soup.find_all("div",class_='block-record-info')
    akwords=soup.find_all("a",class_="snowplow-author-keyword-link")
   # kwords=soup.find_all("a",class_="snowplow-kewords-plus-link")
    info=[]
    for title,name,abstract,akword,kword in zip(titles,names,abstracts,akwords,kwords):
        data={
            'title':title.get_text(),
            'name':list(name.stripped_strings),
            'abstract':abstract.get_text(),
            'akword':akword.get_text(),
            'kword':kword.get_text()
        }
        info.append(data)
    return info

urls=['http://fhya8ff4798d0cae4ed0b725f57cfc9334c1sbpovbf6qwxvx6q9u.fbzz.libproxy.ruc.edu.cn/full_record.do?product=UA&search_mode=AdvancedSearch&qid=1&SID=8FshHtJS1ljw8QxR3z5&page=1&doc={}'.format(str(i)) for i in range(1,30)]
for single_url in urls:
    get_attractions(single_url)


# In[ ]:




