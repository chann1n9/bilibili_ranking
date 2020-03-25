import sys
import time
import os
from bilibili_ranking import BilibiliRanking
from scheduler import Scheduler
from utils.logger import Logger
from plugins.telegram import Telegram
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor


LOG = Logger(package_name='brk')
logger = LOG.get_logger()

def init_dir():
    run_path = os.getcwd()
    path = ['/out', '/out/cache', '/out/logs']
    for i in path:
        if not os.path.exists(run_path + i):
            os.makedirs(run_path + i) 

'''
Scheduler 的Job写在这下面
'''
def job_bilibiliranking():
    BR = BilibiliRanking()
    rv = BR.get_ranking_video()
    BR.input_csv(rv)

def job_telegram():
    BR = BilibiliRanking()
    new_video = BR.bilibili_ranking()
    if new_video is not None:
        tg = Telegram('', '')
        msg = '''
        *有{}个新视频上榜*
        '''.format(str(len(new_video)))
        for v in new_video.values():
            msg+='\n[{}]({})\n作者：{}\n'.format(v['title'], v['link'], v['author'])
        tg.sendmessage(msg)

sche  = BackgroundScheduler()
sche.add_job(job_telegram, 'interval', seconds=5)
sche.start()

    
command = ['help', 'run', 'init', 'test']
# args = sys.argv
args = ['run']
if args[0] == 'help':
    out = '''
    help    Display this page
    run     Run bilibili_ranking
    init    Create neccessary directory
    test    Test
    '''
    print(out)
elif args[0] == 'init':
    init_dir()
elif args[0] == 'run':
    init_dir()
    try:
        while True:
            print('main process')
            time.sleep(60*60)
            # Do something in main process.
    except KeyboardInterrupt:
        logger.info('\nKeyboard Interrupt')
    finally:
        logger.info('Clear the cache..')
        sche.shutdown()
        logger.info('Finished!')
    
else:
    print('python brk.py <command> ["help", "run", "init"]')
