# -*- coding: utf-8 -*-

from app.module.base import BaseController


class RedisController(BaseController):

    def redis_get(self):
        k = self.get('k')
        print(k)
        v = self.redis.get(k)
        return k

    def redis_set(self):
        k = self.get('k')
        v = self.get('v')
        self.redis.set(k, v)
        return self.ok('ok')
