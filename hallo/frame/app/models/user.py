from pymyorm.model import Model
from flask import request, current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
import time
import hashlib


class User(Model):
    tablename = 'user'

    default_password = '123456'

    def set_password(self, password=None):
        if password is None:
            password = self.default_password
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def login(self, expired=None):
        token = self.create_token()
        if expired is None:
            lifetime = app.config.get('PERMANENT_SESSION_LIFETIME')
            if lifetime:
                expired = lifetime.seconds
            else:
                expired = 3600
        app.config['redis'].set(name=token, value=self.id, ex=expired)
        return token

    @staticmethod
    def logout():
        token = request.headers.get('Token')
        app.config['redis'].delete(token)

    def create_token(self):
        md5 = hashlib.md5()
        md5.update(str(time.time()).encode('utf-8'))
        md5.update(str(self.id).encode('utf-8'))
        return md5.hexdigest()
