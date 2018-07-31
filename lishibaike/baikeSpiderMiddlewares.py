# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


from selenium import webdriver
from scrapy.http import HtmlResponse
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class JavaScriptMiddleware(object):
    def process_request(self,request,spider):
        if(spider.name == "lishiBaikeSpider"):
            #print("###############$$$$$$#phantomjs is starting")
            try:
                driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs',service_args=['--ssl-protocol=any'])
                driver.get(request.url)
                time.sleep(1)
                #模拟浏览器滚动到底部
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                time.sleep(3)
                body=driver.page_source
                current_url=driver.current_url
                #print("########################PhantomJS is visting"+request.url)
                #每一个网页的请求都会启动一个phantomjs,用完后就要关闭phantomjs,否则会一直占用内存
                driver.close()
                #print("\t########################PhantomJS is closed")
                return HtmlResponse(current_url,body=body,encoding='utf-8',request=request)
            except:
                return
        else:
            return
