#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import sys 
sys.path.append("lib")
from lib.urlfilter import*
from lib.urlcrawl import*
import os
import os.path
import datetime 
reload(sys)
sys.setdefaultencoding('utf8')  

if __name__ == '__main__':
	starttime=datetime.datetime.now()
	url=raw_input(r'次元の圣光（ex:http://www.exaple.com）>>')
	run_time=int(raw_input(r'次元の沙漏>>'))
	crawl=urlcrawl(url, run_time)
	crawl.crawl()
	endtime=datetime.datetime.now()
	print '时间の轨迹>>'+str((endtime-starttime).seconds)+'s'
	