# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7
#爬取“古诗文网”（http://so.gushiwen.org/gushi/chuntian.aspx）关于春天的古诗，并保存到txt文件中。
# 2.0版独立于1.0版，可以对爬取目标中含有“so”的网页进行爬取。
#2.0版可以提取网页主题作为txt文件的题目。

import requests
from bs4 import BeautifulSoup
import os
import re


url = 'http://so.gushiwen.org/gushi/chuntian.aspx'  # 爬取目标
parser = 'html.parser'
gushi_text=""  #定义参数

# 设置报头,Http协议,增加参数Refer对付防盗链设置
header = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36','Referer': "http:://http://www.mzitu.com/"}

# 解析网页
cur_page = requests.get(url, headers=header)
soup = BeautifulSoup(cur_page.text, parser)
preview_link_list = soup.find(attrs={'class':'typecont'}).find_all('a', target='_blank') # 'class':'typecont'是网址所在网页区域的识别码。有的可能为id=""。
dirname = soup.find('h1').text

#提取主页各诗歌的链接
i=1 #定义计数项
j=len(preview_link_list) #统计需要爬取的网页/诗歌数量

for link in preview_link_list:         #对每个诗歌网页进行爬取
    link = "http://so.gushiwen.org" + link['href']                #提取网页网址
    soup = BeautifulSoup(requests.get(link).text, parser)
    gushi= soup.find(rows="1")  # 提取的内容为古诗内容加上网页链接及一堆乱码
    gushi=gushi.string.split("http:")[0]  # 利用string函数将乱码去除，利用split函数将提取的内容划分为两部分组成的列表，并提取第一部分（古诗内容）
    gushi=re.split(u'——|《|》', gushi)    # 提取的古诗内容为诗句+作者+题目，利用split函数将各部分内容区分开来。
    gushi =list(reversed(gushi))        #将故事内容调整为题目+作者+诗句
    contTotal=""                        #定义变量
    for cont in gushi:                   #将题目、作者和诗句连接为一个string，其间断行。
        contTotal=contTotal+cont+'\n'
    fo=open(dirname+'.txt', 'a')  # 打开文件，r只读，w可写，a追加
    fo.write("第"+str(i)+"首,共"+str(j)+"首")   #写入古诗编号
    fo.write((contTotal + '\n').encode('UTF-8'))  #写入古诗内容
    fo.close        
    print "第"+str(i)+"首完成,共"+str(j)+"首"
    i= i+1
print "完成爬取，请关闭IDLE文档，打开.txt文档查阅！"
  
    





