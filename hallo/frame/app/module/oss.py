# -*- coding: utf-8 -*-

from app.module.base import BaseController
from app.helper.oss import Oss


class OssController(BaseController):

    def upload(self):
        file = self.file('file')
        oss = Oss()
        key = oss.upload(file)

        resp = dict()
        resp['key'] = key
        resp['url'] = oss.url(key)
        resp['sign_url'] = oss.sign_url(key=key, expires=3600)
        return self.ok(resp)
