# -*- coding: utf-8 -*-

from app.module.base import BaseController
from app.models.user import User


class IndexController(BaseController):

    def index(self):
        all = User.find().all(raw=True)
        return self.ok(all)
