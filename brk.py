import sys
import time
import os
import re
import threading
import argparse
from job_master import JobMaster
from utils.logger import Logger
import run_test


LOG = Logger(__name__)
logger = LOG.get_logger()

def init_dir():
    run_path = os.getcwd()
    path = ['/out', '/out/cache', '/out/logs']
    for i in path:
        if not os.path.exists(run_path + i):
            os.makedirs(run_path + i)

def run(jobs_id):
    # Thread APSchedulerThread
    jobmaster = JobMaster()
    if jobs_id:
        jobmaster.load_jobs_by_id(jobs_id)
    else:
        logger.info('load jobs as default..')
        jobmaster.load_jobs()
    jobmaster.start_jobs()
    logger.info('APScheduler is running')

    # Thread MainThread
    logger.info('MainThred is running')
    try:
        TRYTIME = 0
        TIMEOUT = 6
        while True and TRYTIME <= TIMEOUT:
            is_jobs_exist = jobmaster.is_jobs_exist()
            threads = threading.enumerate()
            if not 'APScheduler' in [i._name for i in threads] or not is_jobs_exist:
                logger.warning('APSscheduler is not running or no jobs, Retry...')
                time.sleep(10)
                TRYTIME += 1
                if TRYTIME > TIMEOUT:
                    raise TimeoutError
            else:
                time.sleep(1)
    except TimeoutError:
        logger.error('TIMEOUT, Exit...')
    except KeyboardInterrupt:
        logger.info('Keyboard Interrupt')
    finally:
        logger.info('Clear the cache..')
        logger.info('Finished!')

def test():
    case_list = list()
    for i in run_test.__dict__:
        if re.match(r'^test_\S*', string=i):
            case = getattr(run_test, i)
            case_list.append(case)
    report = ''
    for case in case_list:
        t = case()
        if str(type(t)) != "<class 'NoneType'>":
            msg = t[1] + ' Failed\n----------\n'
            logger.error(msg)
            report += msg
    if report:
        logger.error('Test failed, Exist...')
        exit(0)


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
parser.add_argument('-j', '--job_id', nargs='+', help='指定运行的job id， 默认全部运行')
args = parser.parse_args()
if args.run:
    if args.init:
        init_dir()
    if args.test:
        test()
    elif args.job_id:
        run(jobs_id=args.job_id)
    else:
        DEFAULT = None
        run(jobs_id=DEFAULT)
