# -*- coding: utf-8 -*-

from importlib import import_module


class Console(object):
    def __init__(self):
        pass

    @staticmethod
    def run(command, **kwargs):
        module, action = command.split('/')
        if action.startswith('_'):
            raise Exception(f'protected function is not allowed:{action}')
        try:
            ctrl_list = [ctrl for ctrl in module.split('_')]
            ctrl_file = '_'.join([ctrl for ctrl in ctrl_list])
            m = import_module(f'app.console.{ctrl_file}')
            ctrl_class = ''.join([ctrl.capitalize() for ctrl in ctrl_list])
            c = getattr(m, ctrl_class + 'Command')
            f = getattr(c(), action)
        except Exception as e:
            print(str(e))
            raise e
        f(**kwargs)
