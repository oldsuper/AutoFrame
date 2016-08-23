# -*- coding: UTF-8 -*-
import logging
import logging.config
import os
class Logger():
    def __init__(self):
        print os.getcwd()
        logging.config.fileConfig('../conf/logging.conf')
        self.logger = logging.getLogger('main')
    def debug(self,*msg):
        for m in msg:
            self.logger.debug(m)
    def error(self,*msg):
        for m in msg:
            self.logger.error(m)