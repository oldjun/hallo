# -*- coding: utf-8 -*-

from app.module.base import BaseController


class IndexController(BaseController):

    def index(self):
        tv = dict()
        tv['brief'] = 'Life is short, use python'
        return self.render('index/index.html', tv)
