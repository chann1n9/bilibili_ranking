import os
import requests
from utils.logger import Logger
from requests.exceptions import ProxyError
from plugins.telegram import Telegram
from plugins.bilibili_ranking import BilibiliRanking
from plugins.weather import Weather


LG = Logger(__name__)
logger = LG.get_logger()

def test_telegram_conf():
    tg = Telegram('', '')
    r = tg.get_updates()
    if r is ProxyError:
        logger.error('代理设置错误 {}'.format(tg.proxies))
        return (None, 'test_telegram_conf')
    elif r.status_code == 200:
        logger.debug('telegram 运行正常，可连接')
    else:
        logger.error('telegram 无法连接')
        logger.error('status code: {}'.format(str(r.status_code)))
        return (None, 'test_telegram_conf')

def test_bilibili_ranking():
    br = BilibiliRanking()
    rv = br.get_ranking_video()
    if rv:
        logger.debug('bilibili ranking 运行正常')
    else:
        logger.error('bilibili ranking 没有返回信息')
        return (None, 'test_bilibili_ranking')

def test_weather():
    weather = Weather()
    w = weather.get_weather()
    if w:
        logger.debug('weather 运行正常')
    else:
        logger.error('weather 没有返回信息')
        return (None, 'test_weather')
    