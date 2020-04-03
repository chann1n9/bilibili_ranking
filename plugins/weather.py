import requests
from lxml import etree
import cssselect


class Weather:
    def __init__(self):
        super().__init__()
        self.url = 'https://weather.com/zh-CN/weather/today/l/CHXX0008:1:CH' # 北京天气的url

    def get_weather(self):
        rdict = dict()
        r = requests.get(self.url)
        html = etree.HTML(r.text)
        rdict['位置'] = html.xpath('//h1[@class="h4 today_nowcard-location"]/text()')[0]
        rdict['温度'] = html.xpath('//div[@class="today_nowcard-temp"]/span/text()')[0]
        rdict['体感温度'] = html.xpath('//div[@class="today_nowcard-feels"]/span[@class="deg-feels"]/text()')[0]
        rdict['最高温度'] = html.xpath('//div[@class="today_nowcard-hilo"]/span[@class="deg-hilo-nowcard"]/span/text()')[0]
        rdict['最低温度'] = html.xpath('//div[@class="today_nowcard-hilo"]/span[@class="deg-hilo-nowcard"]/span/text()')[1]
        rdict['紫外线'] = html.xpath('//div[@class="today_nowcard-hilo"]/div/span[@class!="btn-text"]/text()')[0]
        #1 2 4 5 7
        table_list = html.xpath('//div[@class="today_nowcard-sidecar component panel"]//span/text()')
        rdict['风力'] = table_list[0]
        rdict['湿度'] = table_list[1]
        rdict['露点'] = table_list[3]
        rdict['气压'] = table_list[4]
        rdict['能见度'] = table_list[6]

        return rdict
