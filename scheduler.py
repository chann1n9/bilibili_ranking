from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor


class Scheduler():
    def __init__(self):
        super().__init__()
        self.sche = BackgroundScheduler()

    def shutdown_sche(self):
        try:
            self.sche.shutdown()
        except Exception as e:
            raise Exception('Scheduler shutdown failed') from e

    def add_job(self, func):
        self.sche.add_job(func, 'interval', minutes=30)

    def start_jobs(self):
        self.sche.start()

    