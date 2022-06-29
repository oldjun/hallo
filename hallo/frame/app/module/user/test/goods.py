# -*- coding: utf-8 -*-

from app.module.base import BaseController


class GoodsController(BaseController):

    def index(self):
        return 'user/test/goods/index'
