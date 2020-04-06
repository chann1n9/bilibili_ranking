import logging
from logging import handlers
import os


class Logger():
    def __init__(self, module_name):
        super().__init__()

        __DEFAULT_FILE_NAME = 'out/logs/log.log'
        __DEFAULT_WHEN = 'midnight'
        __DEFAULT_BACKUP_COUNT = 30

        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'CRITICAL': logging.CRITICAL
        }
        
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(fmt="%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s - %(message)s",
                                  datefmt="%m/%d/%Y %I:%M:%S %p")

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        self.console = console

        self.is_init_log_exist(__DEFAULT_FILE_NAME)
        file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=__DEFAULT_FILE_NAME,
                when=__DEFAULT_WHEN,
                backupCount=__DEFAULT_BACKUP_COUNT)
        
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.file_handler = file_handler

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console)

    def __del__(self):
        for hdlr in (self.file_handler, self.console):
            self.logger.removeHandler(hdlr)

    def is_init_log_exist(self, log_filename):
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)

    def get_logger(self):
        return self.logger
        