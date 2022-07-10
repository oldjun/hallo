# -*- coding: utf-8 -*-

import logging
import os.path
import shutil
import sys


class Command(object):

    def run(self):
        cmd = 'help'
        if len(sys.argv) > 1:
            cmd = sys.argv[1]
        if cmd in ['help', '--help', '-h']:
            self.help()
        elif cmd in ['version', '--version', '-v']:
            self.version()
        elif cmd == 'create':
            self.create()
        else:
            self.notice(f'{cmd} is not available, Type `hallo help` to see all available commands')

    @staticmethod
    def help():
        print('Available commands:')
        command_list = ['help', 'version', 'create']
        for command in command_list:
            print(command)

    @staticmethod
    def version():
        from hallo import VERSION
        version = '.'.join(str(x) for x in VERSION)
        print(version)

    def create(self):
        if len(sys.argv) < 3:
            self.notice('project name is missing, Type `hallo create project_name`')
            return
        project_name = sys.argv[2]
        project_dir = os.path.join(os.getcwd(), project_name)
        frame_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'frame')
        self.copy_dir(frame_dir, project_dir)
        os.makedirs(os.path.join(project_dir, 'log'))
        os.remove(os.path.join(project_dir, '__init__.py'))

    def notice(self, text):
        print(f'\033[0;31m{text}\033[0m')

    def copy_dir(self, from_file, to_file):
        if not os.path.exists(to_file):
            os.makedirs(to_file)
        files = os.listdir(from_file)
        for f in files:
            if os.path.isdir(f'{from_file}/{f}'):
                self.copy_dir(f'{from_file}/{f}', f'{to_file}/{f}')
            else:
                shutil.copy(f'{from_file}/{f}', f'{to_file}/{f}')
