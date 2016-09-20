# -*- coding: utf-8 -*-
import re
import requests
import shutil
import os
import Queue
from bs4 import BeautifulSoup
import datetime
import urlparse
import urlparse
queone=Queue.Queue(maxsize=0)   #unlimited length
quetwo=Queue.Queue(maxsize=0)   #echecked

req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
'Accept':'text/html;q=0.9,*/*;q=0.8', 
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
		if check_tian_url(queue_temp):
			if check_source_url(queue_temp):
				queueue.put(queue_temp) 

	
    # 把a标签中的href属性值都放进队列一
        
	for url_a in url_data_a:
		queue_temp=url_a.get('href')
		if check_tian_url(queue_temp):
			if check_source_url(queue_temp):
				queueue.put(queue_temp)
	check_repeat_url(queueue)

	# 经检查之后的url放进队列二
    
	# for url_num in range(0,queone.qsize()):   
	# 	queue_temp=queone.get()
	# 	quetwo.put(queue_temp)
	
	#queone->quetwo	
def swap_queue(queone,quetwo):
	while(queone.qsize()):
		quetwo.put(queone.get())

	pass
def check_tian_url(url):
	m=re.match('.*?(\#)',str(url))
	if not m:
		return 1
	else:
		return 0

def analyse_web():
	for url_num in range(0,queone.qsize()):
		spider_web(url_num)
	pass

# 检查url是否属于同源域名        
def check_source_url(url):
	if(url!=None and url!=' '):
		url_source_temp=url.split('.',2)
		#print url_source_temp
		if(url_source_temp[1]==url_aim[1]):
			return 1
		else:
			return 0

		
#检测重复url
def check_repeat_url(quesource):
	url_list=[]
	url_param_list=[]
	time=0
	while(quesource.qsize()):
		queue_temp=quesource.get()
		m=check_param_url(queue_temp)

		#检测网页是否有参数，若有参数获取参数
		if check_param_url(queue_temp):
			url_param_temp=get_param_url(queue_temp)
			if url_param_temp not in url_param_list:
				url_param_list.append(url_param_temp)
				#检测是否url是否重复，若重复则不加入到列表中	
				if queue_temp not in url_list: 
					url_list.append(queue_temp)
					print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
					print url_list
					print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"



		elif queue_temp not in url_list:
			# print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			# print m
			# print "elif"
			# print queue_temp
			# print url_list
			# print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		  	url_list.append(queue_temp)


		
	#把列表中的元素重新放回队列    
	while len(url_list):
		for i in range(0,len(url_list)):
			quesource.put(url_list[i])
			time=time+1
			if time==len(url_list):
				return 
			
#检测参数url
def check_param_url(url):
	if urlparse.urlparse(str(url)).query=='':
		return 0
	else:
		return 1
#获取url参数
def get_param_url(url):
	param_url_temp=urlparse.urlparse(str(url)).query
	m=re.findall('[?|&]*(.*?)=',str(param_url_temp))
	try:
		#print m[0]
		return m[0]
	except:
		return 0
	




def main():
    starttime=datetime.datetime.now()
    urladdress=raw_input(r'次元の圣光（ex:www.exaple.com）>>')
    global url_aim
    url_aim=urladdress.split('.',2)

    global same_url
    same_url='www.('+url_aim[1]+')'#定义同源url规则
    print same_url
    spider_web('http://'+urladdress+'/',queone)
    run_time=int(raw_input(r'次元の沙漏>>'))
    while(run_time-1):
    	print ">>>>>>>"+str(run_time)
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
    check_repeat_url(queone)

    # while(queone.qsize()):
    # 	print queone.get()
    endtime=datetime.datetime.now()
    print '时间の轨迹>>'+str((endtime-starttime).seconds)+'s'
    print quetwo.qsize()
    print queone.qsize()
    while(queone.qsize()):
    	print queone.get()





if __name__ == '__main__':
	main()
