# -*- coding: utf-8 -*-

from app.module.base import BaseController
from flask import session
from app.models.user import User
from app.helper.decorator import check_login


class UserController(BaseController):

    def login(self):
        username = self.post('username')
        password = self.post('password')
        user = User.find().where(username=username).one()
        if not user:
            return self.error('用户不存在')
        if user.password != password:
            return self.error('密码错误')
        session['userid'] = user.id
        return self.ok('登录成功')

    @check_login
    def logout(self):
        session.pop('userid')
        return self.ok('退出成功')

    @check_login
    def info(self):
        userid = session['userid']
        user = User.find().where(id=userid).one()
        if not user:
            return self.error('用户不存在')

        resp = dict()
        resp['userid'] = user.id
        resp['username'] = user.username
        resp['time'] = user.time
        return self.ok(resp)
