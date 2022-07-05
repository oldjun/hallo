# -*- coding: utf-8 -*-

from flask import Flask
from flask_redis import FlaskRedis
from config import config
from app.helper.functions import create_log
from pymyorm.connection_pool import ConnectionPool
import os
import memcache

config_name = os.environ.get('FLASK_APP_CONFIG', 'development')

root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
template_folder = os.path.join(root_path, 'templates')
static_folder = os.path.join(root_path, 'static')

app = Flask(import_name=__name__, template_folder=template_folder, static_folder=static_folder)
app.config.from_object(config[config_name])

# logging
base_path = app.config['BASE_PATH']
log_dir = os.path.join(base_path, 'log')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
log_file = os.path.join(log_dir, 'app.log')
create_log(log_file=log_file)

app.logger.info('flask app init')

debug = app.config.get('DEBUG', False)

# mysql
mysql_conf = app.config.get('MYSQL_CONF')
if mysql_conf:
    pool = ConnectionPool()
    mysql_max_conn = app.config.get('MYSQL_MAX_CONN', 1)
    pool.size(size=mysql_max_conn)
    mysql_conf['debug'] = debug
    pool.create(**mysql_conf)

# redis
app.config['redis'] = FlaskRedis(app)

# cache
cache_conf = app.config.get('CACHE_CONF')
if cache_conf:
    app.config['cache'] = memcache.Client(cache_conf, debug=debug)

from app.router import *
