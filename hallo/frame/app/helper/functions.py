# -*- coding: utf-8 -*-

from logging.config import dictConfig


def ok(data=None):
    if data is None:
        data = 'ok'
    return dict(code=0, data=data)


def error(data=None, code=None):
    if data is None:
        data = 'error'
    if code is None:
        code = 1
    return dict(code=code, data=data)


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
