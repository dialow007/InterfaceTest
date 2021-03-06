import logging
import os
from concurrent_log_handler import ConcurrentRotatingFileHandler
import get_work_dir
from my_util import getConfig


path = get_work_dir.get_base_dir()
log_path = os.path.join(path, 'log')
config_file = os.path.join(path, 'config.yaml')
conf = getConfig.GetConfig(config_file).get_conf("LOG")


class Logger(object):
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        self.log_file_name = os.path.join(log_path, 'log.log')
        self.backup_count = 5
        self.maxBytes = 1024 * 1024 * 10
        self.console_output_level = conf.get('CONSOLE_OUT')
        self.file_output_level = conf.get('FILE_OUT')
        self.formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s  %(message)s')

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回"""
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)
            file_handler = ConcurrentRotatingFileHandler(filename=self.log_file_name,  maxBytes=self.maxBytes,
                                                     backupCount=self.backup_count, encoding="utf-8")
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger
