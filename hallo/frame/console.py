# -*- coding: utf-8 -*-

import sys
from app.helper.console import Console


def main():
    if len(sys.argv) < 2:
        print('参数格式错误!')
        print('正确格式参考: python console.py module/action [--param=value]...')
        return
    command = sys.argv[1]
    args = sys.argv
    args.pop(0)
    args.pop(0)
    params = dict()
    for arg in args:
        if not arg.startswith('--'):
            print('参数格式错误: --param=value')
            return
        arg = arg[2:]
        if not arg.index('='):
            print('参数格式错误: --param=value')
            return
        k, v = arg.split('=')
        params[k] = v
    Console.run(command, **params)


if __name__ == '__main__':
    main()
