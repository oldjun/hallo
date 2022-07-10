# -*- coding: utf-8 -*-

import os
import hashlib
from config import config


class File(object):

    def __init__(self):
        config_name = os.environ.get('FLASK_CONFIG', 'development')
        conf = config[config_name]
        self.base_path = conf.BASE_PATH

        # 设置允许上传的文件类型
        self.file_type_txt = ['text/plain']
        self.file_type_img = ['image/jpeg', 'image/bmp', 'image/png', 'image/gif']
        self.file_type_pdf = ['application/pdf']
        self.file_type_doc = ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        self.file_type_xls = ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
        self.file_type_rar = ['application/x-rar-compressed', 'application/x-7z-compressed', 'application/vnd.rar']

        self.file_path_txt = 'txt'
        self.file_path_img = 'img'
        self.file_path_pdf = 'pdf'
        self.file_path_doc = 'doc'
        self.file_path_xls = 'xls'
        self.file_path_rar = 'rar'

    def upload(self, file):
        if not file:
            raise Exception('文件上传失败')
        path = 'static/upload/'
        if file.content_type in self.file_type_txt:
            path += self.file_path_txt
        elif file.content_type in self.file_type_img:
            path += self.file_path_img
        elif file.content_type in self.file_type_pdf:
            path += self.file_path_pdf
        elif file.content_type in self.file_type_doc:
            path += self.file_path_doc
        elif file.content_type in self.file_type_xls:
            path += self.file_path_xls
        elif file.content_type in self.file_type_rar:
            path += self.file_path_rar
        else:
            raise Exception('不支持该文件类型')

        data = file.read()
        file.seek(0)
        file_md5 = hashlib.md5(data).hexdigest()
        for i in range(0, 4):
            path += '/' + file_md5[i*2:i*2+2]
        disk_path = f'{self.base_path}/{path}'
        if not os.path.exists(disk_path):
            os.makedirs(disk_path)
        ext = file.filename.split('.')[-1]
        file_path = f'{path}/{file_md5}.{ext}'
        real_path = f'{disk_path}/{file_md5}.{ext}'
        file.save(real_path)
        return file_path
