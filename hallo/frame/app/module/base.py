# -*- coding: utf-8 -*-

from flask import request, render_template, current_app as app
from app.models.user import User
import os
import math


class BaseController(object):

    OK = 0
    ERROR = 1

    def __init__(self):
        self.conf = app.config
        self.redis = app.config.get('redis')
        self.cache = app.config.get('cache')
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

    @staticmethod
    def header(name):
        return request.headers.get(name)

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

    @property
    def userid(self):
        token = self.header('Token')
        userid = self.redis.get(token)
        if not userid:
            return None
        return str(userid, 'UTF-8')

    @property
    def user(self):
        userid = self.userid
        if not userid:
            return None
        user = User.find().where(id=userid).one()
        return user
