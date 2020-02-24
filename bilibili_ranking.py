#!/usr/bin/python3
#coding:utf-8 #

import requests
from lxml import etree
import cssselect

'''
说明：
此脚本为爬取bilibili排行榜的新视频，旧的排行榜内容为上一次运行此脚本时生成

运行环境：
请使用python3.6及以上
  请输入以下命令安装依赖包：
    pip3 install -r requirements.txt
  若丢失requirements.txt文件或想单独安装：
    pip3 install requests
	pip3 install lxml
	pip3 install cssselect
    【注意】如果有使用sock5的需求请讲第一条命令改为：
      pip3 install requests[socks]

运行之前：
  请填写下面变量：
    file_path 此变量为脚本生成文件保存路径 【默认】：脚本运行目录
	proxies 代理地址，如果过于频繁使用此脚本被b站封ip，请使用代理  【默认】：空
'''

file_path = ''
proxies = {
	'http:': '',
	'https:': ''
}
headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
}
file_name = '/bilibili_ranking.txt'

def get_content():
	r = requests.get('https://www.bilibili.com/ranking', headers=headers, proxies=proxies)
	html = etree.HTML(r.text)
	return html

def get_ranking_video(html):
	ranking_video = html.cssselect('.rank-list div.content div.info > a')
	rdict = {}
	update_dic = lambda a: {a.text: a.get('href')}
	for a in ranking_video:
		rdict.update(update_dic(a))
	return rdict

def input_file(ranking_video):
	with open(file_path + file_name, 'w+') as f:
		for i in ranking_video:
			f.writelines(i)
			f.write('\n')

def is_new_video_up(ranking_video):
	with open (file_path + file_name, 'r') as f:
		read_file = f.readlines()
		old_video = list(map(lambda x : x.rstrip('\n'), read_file))
	new_video = {k: v for k, v in ranking_video.items() if k not in old_video}
	if new_video == {}:
		return False
	else:
		input_file(ranking_video)
		return new_video

if file_path == '':
	print('【WARNNING】: 脚本生成文件位于执行目录下')
	import os
	file_path = os.getcwd()
	if not os.path.exists(file_path + file_name):
		file = open(file_path + file_name, 'w')
		file.close()

html = get_content()
ranking_video = get_ranking_video(html)
new_video = is_new_video_up(ranking_video)
if not new_video:
	print('还没新视频上榜')
else:
	print('\n有这些新视频上榜【'+ str(len(new_video)) +'】：')
	print('\n=====================================')
	for k, v in new_video.items():
		print('\n' + k + '\n' + v)
