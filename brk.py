from bilibili_ranking import BilibiliRanking
from scheduler import Scheduler
import time


def job():
    BR = BilibiliRanking()
    BR.bilibili_ranking()

sche  = Scheduler()
sche.add_job(job)
sche.start_jobs()

try:
    while True:
        print('main process')
        time.sleep(15 * 60)
        # Do something in main process.
except KeyboardInterrupt:
    print('\nKeyboard Interrupt')
finally:
    print('Clear the cache..')
    sche.shutdown_sche()
    print('Finished!')