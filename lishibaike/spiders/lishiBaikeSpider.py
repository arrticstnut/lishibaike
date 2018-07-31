#!/usr/bin/python
# -*- coding:UTF-8 -*-
# File:    lishiBaikeSpider.py
# Date:    2017-09-17 15:48:03
#
#set default encode as utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import scrapy
import re
import os
import threading
#引入容器
from lishibaike.lishiBaikeItems import LishiBaikeItem

class LishiBaikeSpider(scrapy.Spider):
    #区别不同的spider,名字唯一
    name = "LishiBaikeSpider"
    #允许访问的域
    allowed_domains = ["baike.baidu.com"]
    #爬虫开始地址
    start_urls=['https://baike.baidu.com/item/%E8%B5%A4%E5%A3%81%E4%B9%8B%E6%88%98/81515']

    #####################################################
    levelInfoFileHandle=open('levelInfo.txt','a+')
    ######################################################

    #将人名拼接到链接初始列表
    person_urls=[]
    if os.path.exists('./urlSource/personName.txt'):
        personNamefile=open('./urlSource/personName.txt','r')
        for line in personNamefile:
            personName=line.split()[0]
            personUrl='https://baike.baidu.com/item/'+personName
            #print(personUrl)
            person_urls.append(personUrl)

    #将事件名拼接到链接初始列表
    event_urls=[]
    if os.path.exists('./urlSource/eventName.txt'):
        eventNamefile=open('./urlSource/eventName.txt','r')
        for line in eventNamefile:
            eventName=line.split()[0]
            eventUrl='https://baike.baidu.com/item/'+eventName
            #print(eventUrl)
            event_urls.append(eventUrl)

    #控制爬取的深度
    #原始网页为第一层
    crawlLevelLimit=500

    #获得分类标签的文件,dict用于辅助去重
    labelPath='./label/'

    #总的标签,dict用于辅助去重
    if not os.path.exists(labelPath):
        os.mkdir(labelPath)
    labelAllFileHandle=open(labelPath+'label.All.txt','a+')
    labelAllDict={}
    for line in labelAllFileHandle:
        line=line.strip()
        labelAllDict[line]=1

    #事件使用过的标签,dict用于辅助去重
    labelEventUsed=open(labelPath+'label.EventUsed.txt','a+')
    labelEventUsedDict={}
    for line in labelEventUsed:
        line=line.strip()
        labelEventUsedDict[line]=1
        
    #人物使用过的标签,dict用于辅助去重
    labelPeopleUsedFileHandle=open(labelPath+'label.PeopleUsed.txt','a+')
    labelPeopleUsedDict={}
    for line in labelPeopleUsedFileHandle:
        line=line.strip()
        labelPeopleUsedDict[line]=1

    #允许爬取的标签(全匹配)
    labelYesDict={}
    if os.path.exists(labelPath+'label.Yes.txt'):
        labelYesFileHandle=open(labelPath+'label.Yes.txt','r')
        for line in labelYesFileHandle:
            line=line.strip()
            labelYesDict[line]=1

    #允许爬取的标签(包含匹配)
    labelYesIncludeDict={}
    if os.path.exists(labelPath+'label.YesInclude.txt'):
        labelYesIncludeFileHandle=open(labelPath+'label.YesInclude.txt','r')
        for line in labelYesIncludeFileHandle:
            line=line.strip()
            labelYesIncludeDict[line]=1

    #允许爬取的历史事件的分类标签(全匹配)
    labelEventYesDict={}
    if os.path.exists(labelPath+'label.EventYes.txt'):
        labelEventYesFileHandle=open(labelPath+'label.EventYes.txt','r')
        for line in labelEventYesFileHandle:
            line=line.strip()
            labelEventYesDict[line]=1

    #允许爬取的事件的分类标签(包含匹配)
    labelEventYesIncludeDict={}
    if os.path.exists(labelPath+'label.EventYesInclude.txt'):
        labelEventYesIncludeFileHandle=open(labelPath+'label.EventYesInclude.txt','r')
        for line in labelEventYesIncludeFileHandle:
            line=line.strip()
            labelEventYesIncludeDict[line]=1

    #允许爬取的人物的分类标签(全匹配)
    labelPeopleYesDict={}
    if os.path.exists(labelPath+'label.PeopleYes.txt'):
        labelPeopleYesFileHandle=open(labelPath+'label.PeopleYes.txt','r')
        for line in labelPeopleYesFileHandle:
            line=line.strip()
            labelPeopleYesDict[line]=1

    #允许爬取的人物的分类标签(包含匹配)
    labelPeopleYesIncludeDict={}
    if os.path.exists(labelPath+'label.PeopleYesInclude.txt'):
        labelPeopleYesIncludeFileHandle=open(labelPath+'label.PeopleYesInclude.txt','r')
        for line in labelPeopleYesIncludeFileHandle:
            line=line.strip()
            labelPeopleYesIncludeDict[line]=1

    #不允许爬取的标签(全匹配)
    labelNotDict={}
    if os.path.exists(labelPath+'label.Not.txt'):
        labelNotFileHandle=open(labelPath+'label.Not.txt','r')
        for line in labelNotFileHandle:
            line=line.strip()
            labelNotDict[line]=1

    #不允许爬取的标签(包含匹配)
    labelNotIncludeDict={}
    if os.path.exists(labelPath+'label.NotInclude.txt'):
        labelNotIncludeFileHandle=open(labelPath+'label.NotInclude.txt','r')
        for line in labelNotIncludeFileHandle:
            line=line.strip()
            labelNotIncludeDict[line]=1

    #爬虫入口函数
    def parse(self,response):
        #print("\tTEST1####################")

        #从某一事件页面爬起
        #####################################################
        LishiBaikeSpider.levelInfoFileHandle.write('eventInit'+'\t'+str(0)+'\t'+str(os.getgid())+'\t'+str(threading.current_thread().name)+'\n')
        ######################################################
        yield scrapy.Request(url=response.url, callback=(lambda response,level=1:self.parse_historyPeople(response,level)))

        #从某一人物页面爬起
        #####################################################
        #LishiBaikeSpider.levelInfoFileHandle.write('peopleInit'+'\t'+str(0)+'\n')
        ######################################################
        #yield scrapy.Request(response.url, callback=self.parse_historyPeople)

        #从中国历史事件页面爬起
        #####################################################
        LishiBaikeSpider.levelInfoFileHandle.write('chinaHistoryInit'+'\t'+str(0)+'\t'+str(os.getgid())+'\t'+str(threading.current_thread().name)+'\n')
        ######################################################
        yield scrapy.Request(url="https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%8E%86%E5%8F%B2%E4%BA%8B%E4%BB%B6/1432920?fr=aladdin", callback=self.parse_chinaHiostoryEventUrl)


        #从本地人物和历史事件列表爬起
        for url in LishiBaikeSpider.person_urls:
            #####################################################
            LishiBaikeSpider.levelInfoFileHandle.write('peopleInit'+'\t'+str(0)+'\t'+str(os.getgid())+'\t'+str(threading.current_thread().name)+'\n')
            ######################################################
            yield scrapy.Request(url=url, callback=(lambda response,level=1:self.parse_historyPeople(response,level)))
        for url in LishiBaikeSpider.event_urls:
            #####################################################
            LishiBaikeSpider.levelInfoFileHandle.write('eventInit'+'\t'+str(0)+'\t'+str(os.getgid())+'\t'+str(threading.current_thread().name)+'\n')
            ######################################################
            yield scrapy.Request(url=url, callback=(lambda response,level=1:self.parse_historyEvent(response,level)))
        #yield scrapy.Request(response.url, callback=self.parse_historyEventOnce)

    def parse_chinaHiostoryEventUrl(self,response):
        #找到每个历史时期
        Nodes=response.xpath('//div[@class="para"]')
        for period in Nodes:
            #找到每个时期历史事件的链接
            links=period.xpath('.//@href').extract()
            if(links):
                for url in links:
                    try:
                        url="https://baike.baidu.com"+str(url)
                        #交给解析函数
                        #爬取深度为第一层
                        level=1
                        yield scrapy.Request(url,callback=(lambda response,level=level:self.parse_historyEvent(response,level)))
                    except Exception as e:
                        print (e)



    #此函数是爬取百科词条的基本信息的
    def parse_basicInfo(self,response,item):
        #获得百科词条名字
        item['title']=''
        title=response.xpath('/html/body//div[@class="main-content"]//h1')
        if not title:return #ck
        title=title[0]
        if title:
            titlename=title.xpath('./text()').extract()[0]
            #获得词条名字的注释
            titledesc=title.xpath('./following-sibling::h2')
            if titledesc:
                titledesc=titledesc.xpath('./text()').extract()[0].strip('（').strip('）')
            else:
                titledesc=''
            item['title']=titlename
            item['titledesc']=titledesc

            #获得词条基本信息
            #basicInfos={}
            infostr=''
            basicInfos=response.xpath('//dt[@class="basicInfo-item name"]')
            if basicInfos:
                infostr='{'
                for info in basicInfos:
                    infoname=info.xpath('./text()').extract()[0].strip()
                    #去空白字符,要转成str
                    infoname=re.split('\s| ',str(infoname))
                    infoname=''.join(infoname)

                    infovalue=info.xpath('./following-sibling::dd')[0].xpath('string(.)').extract()[0].strip()
                    #去空白字符
                    infovalue=re.split('\s| ',str(infovalue))
                    infovalue=''.join(infovalue)
                    infostr+=("\"%s\":\"%s\"," % (infoname,infovalue))
                    #basicInfos[infoname]=infovalue
                infostr=infostr.strip(',')+'}'
            #print(infostr)
            item['basicInfos']=infostr


    #此函数是爬取历史事件的
    def parse_historyEvent(self,response,level):
        #实例一个容器，保存爬取的信息

        #####################################################
        LishiBaikeSpider.levelInfoFileHandle.write('event'+'\t'+str(level)+'\t'+str(os.getgid())+'\t'+str(threading.current_thread().name)+'\n')
        ######################################################

        #print("\tTEST3####################")
        item = LishiBaikeItem()
        #解析词条基本信息
        self.parse_basicInfo(response,item)
        #将item作参数时候，是引用传递.(dict是引用传递)
        item['label']="事件"
        yield item
        #控制爬取规模
        #if(level>=LishiBaikeSpider.crawlLevelLimit):return
        try:
            #获取词条id,如https://baike.baidu.com/item/%E8%B5%A4%E5%A3%81%E4%B9%8B%E6%88%98/81515
            #的81515
            #通过“编辑次数”这个节点获取
            urlofId=response.xpath('//*[@class="nslog:1021"]')[0].xpath('./@href').extract()[0]
            itemId=urlofId[urlofId.rfind('/')+1:]
            relatedUrl="https://baike.baidu.com/wikiui/api/zhixinmap?lemmaId="+itemId
            #print("\tTEST**********************************************")
            #print(relatedUrl)
            #爬取相关链接
            yield scrapy.Request(relatedUrl, callback=(lambda response,level=level+1:self.parse_relatedLinks(response,level)))
            #yield scrapy.Request(relatedUrl, callback=self.parse_relatedLinks)
        except Exception as e:
            print (e)

    #爬取深度为一层的相关事件
    def parse_historyEventOnce(self,response):
        #实例一个容器，保存爬取的信息
        item = LishiBaikeItem()
        #解析词条基本信息
        self.parse_basicInfo(response,item)
        #将item作参数时候，是引用传递.(dict是引用传递)
        item['label']="事件"
        yield item


    #此函数是爬取历史人物的
    def parse_historyPeople(self,response,level):
        #实例一个容器，保存爬取的信息

        #####################################################
        LishiBaikeSpider.levelInfoFileHandle.write('people'+'\t'+str(level)+'\t'+str(os.getgid())+'\t'+str(threading.current_thread().name)+'\n')
        ######################################################

        item = LishiBaikeItem()
        #解析词条基本信息
        self.parse_basicInfo(response,item)
        #将item作参数时候，是引用传递.(dict是引用传递)
        item['label']="人物"
        yield item
        #if(level>=LishiBaikeSpider.crawlLevelLimit):return
        try:
            #获取词条id,如https://baike.baidu.com/item/%E8%B5%A4%E5%A3%81%E4%B9%8B%E6%88%98/81515
            #的81515
            itemId=response.url[response.url.rfind('/')+1:]
            relatedUrl="https://baike.baidu.com/wikiui/api/zhixinmap?lemmaId="+itemId
            #爬取相关链接
            #爬取相关链接
            yield scrapy.Request(relatedUrl, callback=(lambda response,level=level+1:self.parse_relatedLinks(response,level)))
            #yield scrapy.Request(relatedUrl, callback=self.parse_relatedLinks)
        except Exception as e:
            print (e)


    #爬取深度为一层的历史人物
    def parse_historyPeopleOnce(self,response):
        #实例一个容器，保存爬取的信息
        item = LishiBaikeItem()
        #解析词条基本信息
        self.parse_basicInfo(response,item)
        #将item作参数时候，是引用传递.(dict是引用传递)
        item['label']="人物"
        yield item


    #既不是历史事件也不是历史人物,用于寻找是否有
    #连接到历史人物和历史事件的链接
    def parse_historyOther(self,response):
        try:
            #获取词条id,如https://baike.baidu.com/item/%E8%B5%A4%E5%A3%81%E4%B9%8B%E6%88%98/81515
            #的81515
            itemId=response.url[response.url.rfind('/')+1:]
            relatedUrl="https://baike.baidu.com/wikiui/api/zhixinmap?lemmaId="+itemId
            #爬取相关链接
            yield scrapy.Request(relatedUrl, callback=self.parse_relatedLinks)
        except Exception as e:
            print (e)


    #解析相关链接
    def parse_relatedLinks(self,response,level):
        if not response: return #ck
        content=json.loads(str(response.text))
        if not content:return #ck
        #content类型是list
        for tip in content:
            #tip是相关链接块，如相关事件，历史人物,类型是dict
            label=tip['tipTitle']#标签,类型是unicode
            label=str(label)
            #所有标签存到文件中，便于人工分类判断
            if not LishiBaikeSpider.labelAllDict.has_key(label):
                LishiBaikeSpider.labelAllDict[label]=1
                LishiBaikeSpider.labelAllFileHandle.write(("%s\t%s\n") % (label,str(level)))
                LishiBaikeSpider.labelAllFileHandle.flush()
            #判断是否有不需要爬取的标签(包含匹配)
            for kNotLabel,v in LishiBaikeSpider.labelNotIncludeDict.items():
                if re.search(kNotLabel,label):
                    return
            #判断是否有不需要爬取的标签(全匹配)
            for kNot,v in LishiBaikeSpider.labelNotDict.items():
                if re.search(kNot,label):
                    return

            data=tip['data']#词条列表，类型是list
            if(label=="相关事件" 
                or label=='历史事件'
                or ((re.search(r'事件$|战争$|战役$|起义',label)))
                #允许爬取的标签的dict,数据来源于本地文件
                or LishiBaikeSpider.labelEventYesDict.has_key(label)
                ):
                #获得使用的标签存到文件中
                if not LishiBaikeSpider.labelEventUsedDict.has_key(label):
                    LishiBaikeSpider.labelEventUsedDict[label]=1
                    LishiBaikeSpider.labelEventUsed.write(("%s\n") % (label))
                    LishiBaikeSpider.labelEventUsed.flush()
                else:
                    LishiBaikeSpider.labelEventUsedDict[label]+=1
                    

                for link in data:
                    #item是每个词条项，类型是dict
                    url=link['url']#词条地址，类型是unicode
                    #yield scrapy.Request(url,callback=self.parse_historyEventOnce)
                    yield scrapy.Request(url, callback=(lambda response,level=level:self.parse_historyEvent(response,level)))
            else:
                if(label=="历史人物"
                    or label=="相关人物"
                    or label=="中国历史人物"
                    or re.search(r'历史人物|政治人物|军事人物|君主|名将|皇帝|帝王|皇后|宰相|将军|大臣',label)
                    or (re.search(r'人物',label) and (not re.search('相关|虚构|虚拟',label)))
                    or LishiBaikeSpider.labelPeopleYesDict.has_key(label)
                    ):
                    #获得使用的标签存到文件中
                    if not LishiBaikeSpider.labelPeopleUsedDict.has_key(label):
                        LishiBaikeSpider.labelPeopleUsedDict[label]=1
                        LishiBaikeSpider.labelPeopleUsedFileHandle.write(("%s\n") % (label))
                        LishiBaikeSpider.labelPeopleUsedFileHandle.flush()
                    else:
                        LishiBaikeSpider.labelPeopleUsedDict[label]+=1
                    #依次调用
                    for link in data:
                        url=link['url']#词条地址，类型是unicode
                        yield scrapy.Request(url, callback=(lambda response,level=level:self.parse_historyPeople(response,level)))
                        #yield scrapy.Request(url,callback=self.parse_historyPeopleOnce)
                else:
                    for link in data:
                        url=link['url']#词条地址，类型是unicode
                        #yield scrapy.Request(url,callback=self.parse_historyOther)

