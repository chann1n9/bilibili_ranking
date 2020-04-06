import requests
import cssselect
import os
import re
import time
from utils import csv_handler
from utils.logger import Logger
from lxml import etree


class BilibiliRanking():
	def __init__(self):
		super().__init__()
		running_path = os.getcwd()
		self.cache_file_path = running_path + '/out/cache/bilibili_ranking.txt'
		self.csv_path = running_path + '/out/'
		self.proxies = {
			'http:': 'http://127.0.0.1:8118',
			'https:': 'http://127.0.0.1:8118'
		}
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
		}
		self.re_c_cache_common_config = re.compile(r'^__\w*__$')
		self.timestamp = float()
		self.__out_file_prefix = 'bilibili_ranking'
		self.LOG = Logger(__name__)
		self.logger = self.LOG.get_logger()

		if not os.path.exists(self.cache_file_path):
			file = open(self.cache_file_path, 'w')
			file.close()

	def __get_content(self):
		r = requests.get('https://www.bilibili.com/ranking', headers=self.headers, proxies=self.proxies)
		html = etree.HTML(r.text)
		return html

	def get_ranking_video(self):
		html = self.__get_content()
		ranking_video_info = html.cssselect('.rank-list div.content div.info')
		self.timestamp = time.time()
		rdict = {
			'__timestamp__': str(self.timestamp)
		}
		av_num_re_compile = re.compile(r'/BV\S*')
		for index, each_video_info in enumerate(ranking_video_info):
			title = each_video_info.cssselect('a.title')[0].text
			link = each_video_info.cssselect('a.title')[0].get('href')
			av_num = av_num_re_compile.search(link).group().lstrip('/') # av号作为id
			play_count, comment_count = each_video_info.xpath('./div[@class="detail"]/span/text()') #我没有办法用cssselector提取”<span><i></i>string</span>“中的文字
			author = each_video_info.xpath('./div[@class="detail"]/a/span/text()')[0]
			author_space = each_video_info.cssselect('div.detail a')[0].get('href')
			pts = each_video_info.cssselect('div.pts > div')[0].text
			video_info = {
				av_num: {
					'rank': str(index + 1),
					'title': title,
					'link': link,
					'play_count': play_count,
					'author': author,
					'author_space': author_space,
					'pts': pts
				}
			}
			rdict.update(video_info)
		return rdict

	def __input_cache_file(self, ranking_video):
		with open(self.cache_file_path, 'w+') as f:
			for i in ranking_video:
				if not self.re_c_cache_common_config.match(i):
					f.writelines(i)
					f.write('\n')

	def is_new_video_up(self, ranking_video):
		with open (self.cache_file_path, 'r') as f:
			read_file = f.readlines()
			old_video = list(map(lambda x : x.rstrip('\n'), read_file))
		new_video = {k: v for k, v in ranking_video.items() if k not in old_video and not self.re_c_cache_common_config.match(k)}
		if not new_video:
			return None
		else:
			self.__input_cache_file(ranking_video)
			return new_video

	# 很多表达式写得太复杂了，需要用到这个方法取重构
	def __get_no_common_conf_dict(self, dic:dict):
		return {k: v for k, v in dic.items() if not self.re_c_cache_common_config.match(k)}

	def input_csv(self, videos_info):
		vi = videos_info
		if self.is_new_video_up(vi) is not None:
			self.logger.info('not none')
			ts = vi['__timestamp__']
			vinfo = self.__get_no_common_conf_dict(vi)
			csv_handler.write_csv(self.csv_path + self.__out_file_prefix + ts + '.csv', vinfo)
			self.logger.info('input csv finished')

	def bilibili_ranking(self):
		ranking_video = self.get_ranking_video()
		new_video = self.is_new_video_up(ranking_video)
		if not new_video:
			self.logger.info('还没新视频上榜')
		else:
			self.logger.info('\n有这些新视频上榜【'+ str(len(new_video)) +'】：')
			self.logger.info('\n=====================================')
			for v in new_video.values():
				self.logger.info('\n' + v['title'] + '\n' + v['link'])
		return new_video
