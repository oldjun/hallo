# -*- coding: utf-8 -*-

import os
import logging
from config import config
from pymyorm.database import Database
from app.helper.functions import create_log


class BaseCommand(object):

    log_file_name = 'console.log'

    def __init__(self):
        config_name = os.environ.get('FLASK_CONFIG', 'development')
        conf = config[config_name]
        self.conf = conf
        self.base_path = conf.BASE_PATH
        self.create_log()
        self.connect()

    def create_log(self):
        log_dir = os.path.join(self.base_path, 'log')
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        log_file = os.path.join(log_dir, self.log_file_name)
        create_log(log_file)

    def connect(self):
        try:
            db_conf = self.conf.DB_CONF
            Database.connect(**db_conf)
        except Exception as e:
            logging.error(str(e))
