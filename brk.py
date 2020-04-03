import sys
import time
import os
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


JobMaster = JobMaster()
JobMaster.load_jobs()
JobMaster.start_jobs()

    
command = ['help', 'run', 'init', 'test']
args = sys.argv
if args[1] == 'help':
    out = '''
    help    Display this page
    run     Run bilibili_ranking
    init    Create neccessary directory
    test    Test
    '''
    print(out)
elif args[1] == 'init':
    init_dir()
elif args[1] == 'run':
    init_dir()
    try:
        while True:
            print('main process still do nothing...')
            time.sleep(60*60)
            # Do something in main process.
    except KeyboardInterrupt:
        logger.info('\nKeyboard Interrupt')
    finally:
        logger.info('Clear the cache..')
        JobMaster.shut_down()
        logger.info('Finished!')
    
else:
    print('python brk.py <command> ["help", "run", "init"]')
