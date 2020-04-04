import sys
import time
import os
import threading
import argparse
from job_master import JobMaster
from utils.logger import Logger


LOG = Logger(package_name='brk')
logger = LOG.get_logger()

def init_dir():
    run_path = os.getcwd()
    path = ['/out', '/out/cache', '/out/logs']
    for i in path:
        if not os.path.exists(run_path + i):
            os.makedirs(run_path + i)

def run():
    # Thread APSchedulerThread
    jobmaster = JobMaster()
    jobmaster.load_jobs()
    jobmaster.start_jobs()

    # Thread MainThread
    try:
        TRYTIME = 0
        TIMEOUT = 10
        while True and TRYTIME <= TIMEOUT:
            is_jobs_exist = jobmaster.is_jobs_exist()
            threads = threading.enumerate()
            if not 'APScheduler' in [i._name for i in threads] or not is_jobs_exist:
                logger.warning('APSscheduler is not running or no jobs, Retry...')
                time.sleep(1)
                TRYTIME += 1
                if TRYTIME > TIMEOUT:
                    raise TimeoutError
    except TimeoutError:
        logger.error('TIMEOUT, Exit...')
    except KeyboardInterrupt:
        logger.info('\nKeyboard Interrupt')
    finally:
        logger.info('Clear the cache..')
        logger.info('Finished!')


APP_DESC="""
Flint 是一个将网页上特定内容爬取，并按时进行推送的机器人。
"""
print(APP_DESC)
if len(sys.argv) == 1:
    sys.argv.append('--help')
parser = argparse.ArgumentParser()
parser.add_argument('run', help='运行打火石')
parser.add_argument('-i', '--init', help='初始化out目录', action='store_true')
parser.add_argument('-t', '--test', help='测试运行', action='store_true')
parser.add_argument('-c', '--conf_path', default=os.getcwd()+'/conf/', help='默认 <程序根目录>/conf，可自定义')
parser.add_argument('-j', '--job', help='指定运行的job名称，默认全部运行')
parser.add_argument('-J', '--job_id', help='指定运行的job id， 默认全部运行')
# parser.add_argument('url',metavar='URL',nargs='+', help="zhubo page URL (http://www.douyutv.com/*/)")
args = parser.parse_args()
if args.run:
    run()
elif args.init:
    init_dir()
    run()
elif args.test:
    pass
elif args.conf_path:
    pass
elif args.job:
    pass
elif args.job_id:
    pass
