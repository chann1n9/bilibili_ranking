import re
import pytz
from plugins.bilibili_ranking import BilibiliRanking
from plugins.telegram import Telegram
from plugins.weather import Weather
from apscheduler.schedulers.background import BackgroundScheduler
from utils import formater


class Jobs:
    
    def bilibiliranking(self):
        BR = BilibiliRanking()
        rv = BR.get_ranking_video()
        BR.input_csv(rv)

    def job_weather(self):
        weather = Weather()
        weather_info = weather.get_weather()
        title = weather_info['位置'] + ': ' + weather_info['温度'] + '摄氏度'
        winfo = {k: v for k, v in weather_info.items() if k != '位置' and k != '温度'}
        tg = Telegram('', '')
        msg = title + '\n'
        for k, v in winfo.items():
            msg+='\n' + k + ': ' + v
        tg.sendmessage_as_text(msg)

    def job_new_ranking_telegram(self):
        BR = BilibiliRanking()
        new_video = BR.bilibili_ranking()
        if new_video is not None:
            for v in new_video.values():
                v['title'] = formater.markdown_v2_formater(v['title'])
                v['author'] = formater.markdown_v2_formater(v['author'])

            tg = Telegram('', '')
            msg = '''
            *有{}个新视频上榜*
            '''.format(str(len(new_video)))
            for v in new_video.values():
                msg+='\n[{}]({})\n作者：{}\n'.format(v['title'], v['link'], v['author'])
            tg.sendmessage_as_markdown(msg)


class JobMaster(Jobs):
    def __init__(self):
        time_zone = pytz.timezone('Asia/Shanghai')
        self.sche = BackgroundScheduler(timezone=time_zone)

    def start_jobs(self):
        self.sche.start()

    def shut_down(self):
        self.sche.shutdown()

    def load_jobs(self):
        self.sche.add_job(self.job_weather, 'cron', hour='9')
        self.sche.add_job(self.job_new_ranking_telegram, 'cron', hour='15,21')
