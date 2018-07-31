#!/usr/bin/python
# -*- coding:UTF-8 -*-
# File:    lishiBaikeItems.py
# Date:    2017-09-17 16:43:27
#

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

class LishiBaikeItem(scrapy.Item):
    #标题
    title = scrapy.Field()
    #标题备注
    titledesc = scrapy.Field()
    #内容
    basicInfos = scrapy.Field()
    #标签
    label = scrapy.Field()
