# -*- coding: utf-8 -*-
import urlparse
import re
from bs4 import BeautifulSoup
import requests
req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
'Accept':'text/html;q=0.9,*/*;q=0.8', 
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding':'gzip', 'Connection':'close', 'Referer':None } 
class urlfilter(object):
	"""docstring for urlfilter"""
	def __init__(self,url):
		super(urlfilter, self).__init__()
		
		self.list=[]
		self.netloc="www.vincebye.top"
		self.url=url


	def clearrepeat(self,list_temp):
		temp=set(list_temp)
		list_temp=[i for i in temp]
		return list_temp

	def checkparams(self,url):
		if urlparse.urlparse(str(url)).query=='':
			return 0
		else:
			return 1
	def getparams(self,url):
		m=re.findall('[?|&]*(.*?)=',str(urlparse.urlparse(str(url)).query))
		try:
			#print m[0]
			return m[0]
		except:
			pass

	def clearsimiliar(self,list_temp):
		url_param_temp=[]
		list_temp_cache=[]
		for i in list_temp:
			if self.checkparams(i):
				if self.getparams(i) not in url_param_temp:
					url_param_temp.append(self.getparams(i))
					list_temp_cache.append(i)
				else:
					pass

			else:
				list_temp_cache.append(i)
		return list_temp_cache

	def sameorigin(self,list_temp):
		list_temp_cache=[]
		for i in list_temp:
			if urlparse.urlparse(str(i)).netloc==self.netloc:
				list_temp_cache.append(i)
			else:
				pass
		return list_temp_cache

	def clearwell(self,list_temp):
		list_temp_cache=[]
		for i in list_temp:
			if not re.match('.*?(\#)',str(i)):
				list_temp_cache.append(i)
			else:
				pass
		return list_temp_cache


	def clearnone(self,list_temp):
		list_temp_cache=[]
		for i in list_temp:
			if not i==None:
				list_temp_cache.append(i)
			else:
				pass
		return list_temp_cache

	def clearurl(self,list_temp):
		list_temp=self.clearnone(list_temp)#clear none
		list_temp=self.clearwell(list_temp)
		list_temp=self.sameorigin(list_temp)
		list_temp=self.clearsimiliar(list_temp)
		list_temp=self.clearrepeat(list_temp)
		return list_temp

	def getlinks(self):
		url_data=[]
		try:
			html=requests.get(str(self.url),headers=req_header).text
		except Exception, e:
			print e
			print 'error'
			return
		soup=BeautifulSoup(html,"lxml")
		url_data_link=soup.find_all('link')#define link url
		url_data_a=soup.find_all('a')#define a url
		url_data_a.extend(url_data_link)
		for i in url_data_a:
			url_data.append(i.get('href'))
		url_data=self.clearurl(url_data)
		self.showurl(url_data)
		

		return url_data

	def showurl(self,list_temp):
		for i in list_temp:
			print i



if __name__ == '__main__':
	url=urlfilter('http://www.vincebye.top')
	url.getlinks()