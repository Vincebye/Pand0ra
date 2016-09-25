# -*- coding: utf-8 -*-
import urlparse
from urlfilter import*
import Queue
#import crash_on_ipy
import copy
import datetime

list_temp=[]
list_temp_cache=[]
queueone=Queue.Queue(maxsize=0)
class urlcrawl():
	"""docstring for ClassName"""
	def __init__(self,url,time):
		#super(ClassName, self).__init__()
		#self.arg = arg
		self.url=url
		self.time=time

	def crawl(self):
		global list_temp
		global list_temp_cache
		url=self.url
		time=self.time

		m_urlfilter=urlfilter(url)
		if time==1:
			list_temp.extend(m_urlfilter.getlinksforlist(url))
			for i in list_temp:
				print i
		else:
			list_temp.extend(m_urlfilter.getlinksforlist(url))
			while(time-1):
				list_temp.extend(m_urlfilter.getalllinksforlist(list_temp))
				time=time-1
			#list_temp=copy.deepcopy(m_urlfilter.clearurl(list_temp_cache))
			list_temp=copy.deepcopy(m_urlfilter.clearurl(list_temp))
			print 'aim>>'+str(len(list_temp))
			for i in list_temp:
				print i

				
		
if __name__ == '__main__':
	starttime=datetime.datetime.now()
	url=raw_input(r'次元の圣光（ex:http://www.exaple.com）>>')
	run_time=int(raw_input(r'次元の沙漏>>'))
	crawl=urlcrawl(url, run_time)
	crawl.crawl()
	endtime=datetime.datetime.now()
	print '时间の轨迹>>'+str((endtime-starttime).seconds)+'s'
	# urlwqw=urlfilter('http://www.vincebye.top')
	# print urlwqw.getlinksforlist()
	