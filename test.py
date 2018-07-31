#!/usr/bin/python
# -*- coding:UTF-8 -*-
# File:    test.py
# Date:    2017-12-01 15:17:32
#
import os

def watch_dir_filename(dirPath):
    for curDir,subDirs,subFiles in os.walk(dirPath):
        print (curDir) #当前路径
        print (subDirs) #所有子目录
        print (subFiles) #所有子文件

def listDir(path):
    for file in os.listdir(path):
        print (file)



dirPath = './'
watch_dir_filename(dirPath)
listDir(dirPath)
