# -*- coding: utf-8 -*-

import os
import warnings
from datetime import timedelta

warnings.filterwarnings('ignore')


class Config(object):
    ENV = 'development'
    DEBUG = False
    TESTING = False
    HOST = '127.0.0.1'
    PORT = 80
    # SERVER_NAME = 'hallo.com'
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))

    # session
    SECRET_KEY = ''
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    # file upload
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8M

    # mysql
    MYSQL_POOL_SIZE = 1
    MYSQL_CONF = dict(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='password',
        database='hallo',
        charset='utf8'
    )

    # redis
    REDIS_URL = 'redis://127.0.0.1:6379/0'

    # cache
    CACHE_CONF = [
        '127.0.0.1:11211'
    ]

    # oss
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
    MYSQL_POOL_SIZE = 8
    MYSQL_CONF = dict(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='password',
        database='hallo',
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
