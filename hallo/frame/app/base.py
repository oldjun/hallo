# -*- coding: utf-8 -*-

import logging
from flask import Flask
from flask_redis import FlaskRedis
from importlib import import_module
from app.helper.functions import error, create_log
from app.helper.decorator import time_cost, assign_connection
from config import config
from pymyorm.connection_pool import ConnectionPool
import os

config_name = os.environ.get('FLASK_APP_CONFIG', 'development')

root_path = os.path.dirname(os.path.dirname(__file__))
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

# mysql
mysql_conf = app.config.get('MYSQL_CONF')
if mysql_conf:
    pool = ConnectionPool()
    mysql_max_conn = app.config.get('MYSQL_MAX_CONN', 1)
    pool.size(size=mysql_max_conn)
    mysql_conf = mysql_conf
    debug = app.config.get('DEBUG', False)
    mysql_conf['debug'] = debug
    pool.create(**mysql_conf)

# redis
app.config['redis'] = FlaskRedis(app)


# dynamic router
@app.route('/', methods=['GET', 'POST'])
@app.route('/<module>', methods=['GET', 'POST'])
@app.route('/<module>/<controller>', methods=['GET', 'POST'])
@app.route('/<module>/<controller>/<action>', methods=['GET', 'POST'])
@time_cost
@assign_connection
def dispatcher(module='index', controller='index', action='index'):
    try:
        ctrl_list = [ctrl for ctrl in controller.split('-')]
        ctrl_file = '_'.join([ctrl for ctrl in ctrl_list])
        m = import_module(f'app.module.{module}.{ctrl_file}')
        ctrl_class = ''.join(ctrl.capitalize() for ctrl in ctrl_list)
        c = getattr(m, ctrl_class + 'Controller')
        method = action.replace('-', '_')
        f = getattr(c(), method)
        return f()
    except Exception as e:
        logging.error(str(e))
        return error(str(e))
