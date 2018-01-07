# -*- coding:utf-8 -*-

import url_manager, html_downloader, html_parser, html_outputer

class SpyderMain(object):
	def __init__(self):
		self.urls = url_manager.UrlManager()				#管理器
		self.downloader = html_downloader.HtmlDownloader()	#下载器
		self.parser = html_parser.HtmlParser()				#解析器
		self.outputer = html_outputer.HtmlOutputer()		#输出器
		
	def craw(self, root_url):
		count = 1
		self.urls.add_new_url(root_url)						#添加第一个url
		while self.urls.has_new_url():
			try:											#异常处理
				new_url = self.urls.get_new_url()
				print ("craw %d : %s"%(count, new_url))		#打印第n个url
				html_cont = self.downloader.download(new_url)
				new_urls, new_data = self.parser.parse(new_url, html_cont)
				self.urls.add_new_urls(new_urls)
				self.outputer.collect_data(new_data)
				
				if count == 1000:							#1000个结束
					break
						
				count = count + 1
			except:
				print ("craw failed")
			
		self.outputer.output_html()

if __name__=="__main__":
	root_url = "https://baike.baidu.com/item/Python"		#主函数从python开始爬
	obj_spyder = SpyderMain()
	obj_spyder.craw(root_url)