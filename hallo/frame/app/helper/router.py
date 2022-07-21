# -*- coding: utf-8 -*-

import logging
from importlib import import_module
from flask import redirect
from app.helper.functions import error
from app.helper.decorator import time_cost, assign_connection


class Router(object):

    def __init__(self, app, subdomain=None, module=None):
        self.app = app
        self.subdomain = subdomain
        self.module = module

        @self.app.route('/<path:path>', methods=['GET', 'POST'], endpoint=module, subdomain=subdomain)
        @time_cost
        @assign_connection
        def default(path):
            arr = path.split('/')
            if len(arr) < 2:
                return error('404 Not Found.')
            action = arr[-1]
            arr.pop()
            controller = arr[-1]
            arr.pop()
            if module:
                module_arr = module.split('/')
                __module = '.'.join(module_arr + arr)
            else:
                __module = '.'.join(arr)
            return self.dispatcher(__module, controller, action)

        # handle the favicon request
        if self.module:
            favicon_endpoint = module + '/favicon'
        else:
            favicon_endpoint = 'favicon'

        @app.route('/favicon.ico', methods=['GET', 'POST'], endpoint=favicon_endpoint, subdomain=subdomain)
        def favicon():
            return redirect('/static/favicon.ico')

    def add(self, path, handler, methods=None):
        if methods is None:
            methods = ['GET', 'POST']

        array = handler.split('/')
        if self.module:
            array.insert(0, self.module)
        handler = '/'.join(array)

        @self.app.route(path, methods=methods, endpoint=handler, subdomain=self.subdomain)
        @time_cost
        @assign_connection
        def route(**kwargs):
            arr = handler.split('/')
            action = arr[-1]
            arr.pop()
            controller = arr[-1]
            arr.pop()
            module = '.'.join(arr)
            return self.dispatcher(module, controller, action, **kwargs)

    @staticmethod
    def dispatcher(module='', controller='index', action='index', **kwargs):
        try:
            ctrl_list = [ctrl for ctrl in controller.split('-')]
            ctrl_file = '_'.join([ctrl for ctrl in ctrl_list])
            if module:
                module = module.replace('-', '_')
                module_name = f'app.module.{module}.{ctrl_file}'
            else:
                module_name = f'app.module.{ctrl_file}'
            m = import_module(module_name)
            ctrl_class = ''.join(ctrl.capitalize() for ctrl in ctrl_list)
            c = getattr(m, ctrl_class + 'Controller')
            method = action.replace('-', '_')
            f = getattr(c(), method)
            return f(**kwargs)
        except Exception as e:
            logging.error(str(e))
            return error(str(e))
