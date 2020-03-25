import logging
from logging import handlers
import os


'''
默认保留30天日志，每天0点创建新的log文件
'''

class Logger():
    def __init__(self, package_name, **kwargs):
        super().__init__()

        __DEFAULT_FILE_NAME = 'out/logs/log.log'
        __DEFAULT_WHEN = 'midnight'
        __DEFAULT_INTERVAL = None
        __DEFAULT_BACKUP_COUNT = 30
        __DEFAULT_CONSOLE_LEVEL = 'DEBUG'
        __DEFAULT_FILE_LEVEL = 'DEBUG'

        kw = {
            'file_level' : None or __DEFAULT_FILE_LEVEL,
            'console_level' : None or __DEFAULT_CONSOLE_LEVEL,
            'filename' : None or __DEFAULT_FILE_NAME,
            'when' : None or __DEFAULT_WHEN,
            'interval' : None or __DEFAULT_INTERVAL,
            'backupCount' : None or __DEFAULT_BACKUP_COUNT
        }

        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'CRITICAL': logging.CRITICAL
        }

        for i in kwargs:
            if i in kw:
                kw[i] = kwargs[i]
        
        self.logger = logging.getLogger(package_name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(fmt="%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s - %(message)s",
                                  datefmt="%m/%d/%Y %I:%M:%S %p")

        console = logging.StreamHandler()
        console.setLevel(levels[kw.get('console_level')])
        console.setFormatter(formatter)
        self.console = console

        self.is_init_log_exist(__DEFAULT_FILE_NAME)
        file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=__DEFAULT_FILE_NAME,
                when=__DEFAULT_WHEN,
                backupCount=__DEFAULT_BACKUP_COUNT)
        # try:
        #     file_handler = logging.handlers.TimedRotatingFileHandler(
        #         filename=__DEFAULT_FILE_NAME,
        #         when=kw.get('when'),
        #         interval=kw.get('interval'),
        #         backupCount=kw.get('backupCount'))
        # except TypeError:
        #     file_handler = logging.handlers.TimedRotatingFileHandler(
        #         filename=__DEFAULT_FILE_NAME,
        #         when=kw.get('when'),
        #         backupCount=kw.get('backupCount'))
        
        file_handler.setLevel(levels[kw.get('file_level')])
        file_handler.setFormatter(formatter)
        self.file_handler = file_handler

        # if package_name not in self.logger.handlers:
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console)

    def __del__(self):
        self.remove_handler()

    def is_init_log_exist(self, log_filename):
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)

    def get_logger(self):
        return self.logger

    def remove_handler(self):
        for hdlr in (self.file_handler, self.console):
            self.logger.removeHandler(hdlr)


        