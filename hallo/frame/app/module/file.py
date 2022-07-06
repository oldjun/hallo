# -*- coding: utf-8 -*-

from app.module.base import BaseController
from app.helper.file import File


class FileController(BaseController):

    def upload(self):
        file = self.file('file')
        f = File()
        path = f.upload(file)

        resp = dict()
        resp['path'] = path
        return self.ok(resp)
