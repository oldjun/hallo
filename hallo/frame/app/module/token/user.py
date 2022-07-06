# -*- coding: utf-8 -*-

from app.module.base import BaseController
from app.module.user import User
from app.helper.decorator import check_token


class UserController(BaseController):

    def login(self):
        username = self.post('username')
        password = self.post('password')
        user = User.find().where(username=username).one()
        if not user:
            return self.error('用户不存在')
        if user.password != password:
            return self.error('密码错误')
        token = user.login()
        resp = dict()
        resp['token'] = token
        return self.ok(resp)

    @check_token
    def logout(self):
        self.user.logout()
        return self.ok('退出成功')

    @check_token
    def info(self):
        user = self.user

        resp = dict()
        resp['userid'] = user.id
        resp['username'] = user.username
        resp['time'] = user.time
        return self.ok(resp)
