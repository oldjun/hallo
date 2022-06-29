# -*- coding: utf-8 -*-

from app.module.base import BaseController


class IndexController(BaseController):

    def index(self):
        return 'admin/index/index'
