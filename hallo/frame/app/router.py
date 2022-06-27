# -*- coding: utf-8 -*-

from app.base import app
from app.helper.router import Router

router = Router(app)
router.add('/', 'index/index')
router.add('/test/<name>', 'test/hello')
