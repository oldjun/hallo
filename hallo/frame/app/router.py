# -*- coding: utf-8 -*-

from app.base import app
from app.helper.router import Router


router = Router(app=app)
router.add('/', 'index/index')
