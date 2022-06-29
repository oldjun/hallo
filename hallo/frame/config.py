# -*- coding: utf-8 -*-

import os
import warnings

warnings.filterwarnings('ignore')


class Config(object):
    ENV = 'development'
    DEBUG = False
    TESTING = False
    HOST = '127.0.0.1'
    PORT = 80
    SERVER_NAME = 'hallo.com'
    SECRET_KEY = ''
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))

    # mysql config
    MYSQL_MAX_CONN = 1
    # MYSQL_CONF = dict(
    #     host='127.0.0.1',
    #     port=3306,
    #     user='root',
    #     password='password',
    #     database='hallo',
    #     charset='utf8'
    # )

    # redis config
    REDIS_URL = 'redis://127.0.0.1:6379/0'

    # oss config
    OSS_CONF = dict(
        endpoint='',
        bucket='',
        access_key_id='',
        access_key_secret=''
    )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    ENV = 'production'
    MYSQL_MAX_CONN = 8
    MYSQL_CONF = dict(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='password',
        database='rabble',
        charset='utf8'
    )


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True


config = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
    testing=TestingConfig
)
