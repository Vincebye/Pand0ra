# -*- coding: utf-8 -*-
import re
import requests
import shutil
import os
import Queue
from bs4 import BeautifulSoup

same_url="www.(vincebye)"#定义同源url规则
req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept':'text/html;q=0.9,*/*;q=0.8', 
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding':'gzip', 'Connection':'close', 'Referer':None } 



def spider_web(url):
	html=requests.get(url,headers=req_header).text
	soup=BeautifulSoup(html,"lxml")
	queone=Queue.Queue(maxsize=0)   #unlimited length
	quetwo=Queue.Queue(maxsize=0)   #echecked
	url_data_link=soup.find_all('link')#define link url
	url_data_a=soup.find_all('a')#define a url
	url_data_script=soup.find_all('src') #..#js url
	i=0

    
    # 把link标签的href属性都放进队列一
    
	for url_link in url_data_link:
		if not(str(url_link).isspace()):
		    queone.put(url_link.get('href')) 

	
    # 把a标签中的href属性值都放进队列一
        
	for url_a in url_data_a:
		if not(str(url_a).isspace()):
		    queone.put(url_a.get('href'))     

    
    # 经检查之后的url放进队列二
    
	for url_num in range(0,queone.qsize()):   
		queue_temp=queone.get()
		if check_url(queue_temp):
			quetwo.put(queue_temp)
			print quetwo.get()

	
    # 检查url是否属于同源域名
        
def check_url(url):
	if(url!=None):
		return re.search(same_url, url)



if __name__ == '__main__':
	spider_web('http://www.vincebye.top')
