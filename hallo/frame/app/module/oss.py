# -*- coding: utf-8 -*-

from app.module.base import BaseController
from app.helper.oss import Oss


class FileController(BaseController):

    def upload(self):
        file = self.file('file')
        oss = Oss()
        key = oss.upload(file)

        resp = dict()
        resp['key'] = key
        resp['url'] = oss.url(key)
        resp['sign_url'] = oss.sign_url(key)
        return self.ok(resp)
