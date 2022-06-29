# -*- coding: utf-8 -*-

from app.base import app
from app.helper.router import Router


router = Router(app=app)
router.add('/', 'index/index')
router.add('/test/<name>', 'test/hello')

admin = Router(app=app, subdomain='admin', module='admin')
admin.add('/', 'index/index')

user = Router(app=app, subdomain='user', module='user/test')
user.add('/', 'index/index')
