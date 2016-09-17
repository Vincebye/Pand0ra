# -*- coding: utf-8 -*-
import re
import requests
import shutil
import os
import Queue
from bs4 import BeautifulSoup
import copy
same_url="www.(vincebye)"#定义同源url规则
queone=Queue.Queue(maxsize=0)   #unlimited length
quetwo=Queue.Queue(maxsize=0)   #echecked

req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept':'text/html;q=0.9,*/*;q=0.8', 
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding':'gzip', 'Connection':'close', 'Referer':None } 



def spider_web(url,queueue):
	try:
	    html=requests.get(url,headers=req_header).text
	except Exception, e:
		return
	finally:
		pass
	html=requests.get(url,headers=req_header).text
	soup=BeautifulSoup(html,"lxml")
	# queone=Queue.Queue(maxsize=0)   #unlimited length
	# quetwo=Queue.Queue(maxsize=0)   #echecked
	url_data_link=soup.find_all('link')#define link url
	url_data_a=soup.find_all('a')#define a url
	url_data_script=soup.find_all('src') #..#js url
	i=0

    
    # 把link标签的href属性都放进队列一
    
	for url_link in url_data_link:
		queue_temp=url_link.get('href')
		if check_url(queue_temp):
		    queueue.put(queue_temp) 

	
    # 把a标签中的href属性值都放进队列一
        
	for url_a in url_data_a:
		queue_temp=url_a.get('href')
		if check_url(queue_temp):
		    queueue.put(queue_temp)     

    # 经检查之后的url放进队列二
    
	# for url_num in range(0,queone.qsize()):   
	# 	queue_temp=queone.get()
	# 	quetwo.put(queue_temp)
	
#将队列一的值传给队列二	
def swap_queue(queone,quetwo):
	while(queone.qsize()):
		quetwo.put(queone.get())

	pass

def analyse_web():
	for url_num in range(0,queone.qsize()):
		spider_web(url_num)
	pass

def main():
    spider_web('http://www.vincebye.top',queone)
    run_time=int(raw_input(r'pleasw input'))
    while(run_time):
        while(queone.qsize()):
        	try:
        		spider_web(queone.get(), quetwo)
        	except Exception, e:
        		print "error"
        		break
        	finally:
        		pass
        swap_queue(quetwo, queone)
        run_time=run_time-1

    # while(queone.qsize()):
    # 	print queone.get()
    print quetwo.qsize()
    print queone.qsize()
    # 检查url是否属于同源域名
        
def check_url(url):
	if(url!=None):
		return re.search(same_url, url)



if __name__ == '__main__':
	main()
