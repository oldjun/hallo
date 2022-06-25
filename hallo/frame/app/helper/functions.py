# -*- coding: utf-8 -*-

import hashlib
import time
from logging.config import dictConfig


def ok(data='ok'):
    return dict(code=0, data=data)


def error(data='error', code=1):
    return dict(code=code, data=data)


def create_token(userid):
    md5 = hashlib.md5()
    md5.update(str(time.time()).encode('utf-8'))
    md5.update(userid.encode('utf-8'))
    return md5.hexdigest()


def create_log(log_file):
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)s [%(filename)s:%(lineno)s]: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'message': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': log_file,
                'maxBytes': 1024 * 1024,
                'backupCount': 10,
                'encoding': 'utf-8'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi', 'message']
        }
    })
