# -*- coding: utf-8 -*-

import functools
import time
import logging
from flask import request, session, current_app as app
from app.helper.functions import error
from pymyorm.local import local
from pymyorm.connection_pool import ConnectionPool


# assign one connection to the request
def assign_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pool = ConnectionPool()
        try:
            local.conn = pool.get()
            return func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            # don't forget to put connection into pool
            pool.put(local.conn)
    return wrapper


def check_login(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        userid = session.get('userid')
        if not userid:
            return error('login is required', 401)
        else:
            return func(*args, **kwargs)
    return wrapper


def check_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Token')
        if not token:
            return error('token is missing', 401)
        if not app.config['redis'].get(token):
            return error('token is expired', 401)
        else:
            return func(*args, **kwargs)
    return wrapper


def time_cost(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        resp = func(*args, **kwargs)
        end = time.time()
        cost = round(end - start, 3)
        logging.info(f'{request.path} time cost={cost}s')
        return resp
    return wrapper


def retry(num=1, seconds=0):
    def outer(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            for i in range(0, num):
                try:
                    resp = func(*args, **kwargs)
                    if resp['code'] == 0:
                        return resp
                    if seconds > 0:
                        time.sleep(seconds)
                except Exception as e:
                    logging.error(str(e))
            return error(f'retry {num} times and failed')
        return inner
    return outer
