#!/usr/bin/python
# -*- coding:UTF-8 -*-
# File:    baikeSpiderPipelines.py
# Date:    2017-09-18 21:05:15
#
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from scrapy.exceptions import DropItem
import json
import re
import os
import threading

class BaikeSpiderPipeline(object):
    #记录写入文件的词条数量
    itemCount=0
    #单个文件保存条目数量上限
    itemLimit=10000
    #文件编号
    itemFileNum=1
    #创建保存数据的文件夹
    dataPath="./data/"
    threadIdInfoPipelineFileHandle=open('threadIdInfoPipleline.txt','a+')
    if not (os.path.exists(dataPath)):
        os.mkdir(dataPath)
    def __init__(self):
        #打开文件
        self.file = open(BaikeSpiderPipeline.dataPath+'data_1.txt','w+')

    #实现处理数据的process_item方法
    def process_item(self,item,spider):
        #没有所需信息
        if item['title'] and item['basicInfos']:
            #写入文件
            ###################################################################################################################
            BaikeSpiderPipeline.threadIdInfoPipelineFileHandle.write(str(os.getgid())+'\t'+str(threading.current_thread().name)+'\n')
            ###################################################################################################################
            basicinfo=item['basicInfos'].strip('{').strip('}')
            if(item['titledesc']):
                basicinfo=("\"remark\":\"%s\"," % (item['titledesc']))+basicinfo
            basicinfo=("\"label\":\"%s\"," % (item['label']))+basicinfo
            basicinfo='{'+basicinfo+'}'
            '''
            print(basicinfo)
            '''

            if( BaikeSpiderPipeline.itemCount >= BaikeSpiderPipeline.itemLimit):
                #已经写满一个文件
                self.file.close()
                BaikeSpiderPipeline.itemFileNum+=1
                filename=BaikeSpiderPipeline.dataPath+"data_"+str(BaikeSpiderPipeline.itemFileNum)+".txt"
                #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",filename)
                self.file = open(filename,'w+')
                self.file.write("{\"%s\":%s}\n" % (item['title'],basicinfo))
                #刷新
                self.file.flush()
                BaikeSpiderPipeline.itemCount=1
            else:
                #print("@@@@@@@@@@@@hello world!@@@@@@@@@@@@@@@@@",self.file.name)
                self.file.write("{\"%s\":%s}\n" % (item['title'],basicinfo))
                #刷新
                self.file.flush()
                BaikeSpiderPipeline.itemCount+=1
            #self.file.close()
        return item

    #该方法在spider被开启时被调用
    def open_spider(self,spider):
        pass
    #该方法在spider被关闭时被调用
    def close_spider(self,spider):
        pass
