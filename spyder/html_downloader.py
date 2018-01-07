# -*- coding:utf-8 -*-
import urllib.request

class HtmlDownloader(object):


	def download(self, url):
		if url is None:
			return None
			
		response = urllib.request.urlopen(url)		#urllib2里面一个简单的函数
		
		if response.getcode() != 200:				#判断是否连接上
			return None
			
		
		return response.read()