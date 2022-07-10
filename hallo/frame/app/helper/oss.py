# -*- coding: utf-8 -*-

import os
import oss2
import hashlib
from config import config


class Oss(object):

    def __init__(self):
        config_name = os.environ.get('FLASK_CONFIG', 'development')
        conf = config[config_name]
        self.conf = conf
        self.auth = oss2.Auth(conf.OSS_CONF['access_key_id'], conf.OSS_CONF['access_key_secret'])
        self.bucket = oss2.Bucket(self.auth, conf.OSS_CONF['endpoint'], conf.OSS_CONF['bucket'])

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

    def put(self, key, data):
        self.bucket.put_object(key=key, data=data)

    def get(self, key):
        data = self.bucket.get_object(key).read()
        return data.decode('utf-8')

    def delete(self, key):
        self.bucket.delete_object(key)

    def url(self, key):
        url = f"http://{self.conf.OSS_CONF['bucket']}.{self.conf.OSS_CONF['endpoint']}/{key}"
        return url

    def sign_url(self, key, expires):
        url = self.bucket.sign_url(method='GET', key=key, expires=expires, slash_safe=True)
        return url

    def upload(self, file):
        if not file:
            raise Exception('文件上传失败')
        path = ''
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
        file_md5 = hashlib.md5(data).hexdigest()
        for i in range(0, 4):
            path += '/' + file_md5[i*2:i*2+2]
        ext = file.filename.split('.')[-1]
        key = f'{path}/{file_md5}.{ext}'
        self.put(key, data)
        return key
