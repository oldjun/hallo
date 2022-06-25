# -*- coding: utf-8 -*-

from flask import request, render_template, current_app as app
import json
import math


class BaseController(object):

    OK = 0
    ERROR = 1

    def __init__(self):
        self.conf = app.config
        self.redis = app.config['redis']
        self.page = 0
        self.offset = 0
        self.limit = 0

    @staticmethod
    def ok(data, code=OK):
        return dict(code=code, data=data)

    @staticmethod
    def error(data, code=ERROR):
        return dict(code=code, data=data)

    @staticmethod
    def get(name):
        return request.args.get(name)

    @staticmethod
    def post(name):
        return request.json.get(name)

    @staticmethod
    def render(template, data=None):
        if data is None:
            return render_template(template)
        else:
            return render_template(template, **data)

    def init_page(self):
        self.page = int(request.args.get('page', 1))
        self.limit = int(request.args.get('limit', 10))
        self.offset = (self.page - 1) * self.limit

    def resp_list(self, all, total):
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
