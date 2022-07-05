# -*- coding: utf-8 -*-

from flask import request, render_template, current_app as app
import os
import json
import math


class BaseController(object):

    OK = 0
    ERROR = 1

    def __init__(self):
        self.conf = app.config
        self.redis = app.config['redis']
        self.memcache = app.config['memcache']
        self.page = 0
        self.offset = 0
        self.limit = 0

    @staticmethod
    def ok(data=None, code=OK):
        if data is None:
            data = 'ok'
        return dict(code=code, data=data)

    @staticmethod
    def error(data=None, code=ERROR):
        if data is None:
            data = 'error'
        return dict(code=code, data=data)

    @staticmethod
    def get(name):
        return request.args.get(name)

    @staticmethod
    def post(name):
        return request.json.get(name)

    @staticmethod
    def file(name):
        return request.files.get(name)

    def render(self, template, data=None):
        base_path = self.conf.get('BASE_PATH')
        filename = os.path.join(base_path, 'templates', template)
        if not os.path.exists(filename):
            raise Exception(f'file not found: {filename}')
        if data is None:
            return render_template(template)
        else:
            return render_template(template, **data)

    def init_page(self):
        self.page = int(request.args.get('page', 1))
        self.limit = int(request.args.get('limit', 10))
        self.offset = (self.page - 1) * self.limit

    def resp_page(self, all, total):
        total_page = math.ceil(total / self.limit)
        data = dict(
            list=all,
            page=self.page,
            limit=self.limit,
            total=total,
            total_page=total_page
        )
        return self.ok(data)

    def get_current_user(self):
        token = request.headers.get('Token')
        user = self.redis.get(token)
        return json.loads(user)
