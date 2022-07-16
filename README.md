Hallo
---
Table of Contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Documentation](#documentation)
* [Example](#example)
* [Resources](#resource)
* [License](#license)

web mvc framework for python

## <a href=#requirements>Requirements</a>

* Python:
    *  [CPython](https://www.python.org/): 3.6 or newer

## <a href=#installation>Installation</a>

Package is uploaded on [PyPI](https://pypi.org/project/PyMyORM/).

You can install it with pip:

```shell
$python3 pip install hallo
```

## <a href=#documentation>Documentation</a>
[中文文档](https://hkrb7870j3.feishu.cn/docx/doxcnqVfgeBtBJP3aHku4zJ71ab).

## <a href=#example>Example</a>

### show version

```shell
hallo --version
```

### create project

```shell
hallo create your-project
```

### install requirements

```shell
cd your-project
pip install -r requirements.txt
```

### run project

```shell
python main.py
```

### create first controller

file: module/hello.py

```python
from app.module.base import BaseController

class HelloController(BaseController):

    def world(self):
        return 'hello world'
```

### create json controller

file: module/json.py

```python
from app.module.base import BaseController

class JsonController(BaseController):

    def this_is_ok(self):
        return self.ok('this is ok')

    def this_is_error(self):
        return self.error('this is error')
```

### create html controller

file: module/html.py

```python
from app.module.base import BaseController

class HtmlController(BaseController):
    
    def index(self):
        return self.render('html/index.html')
```

### config

development

```python
class DevelopmentConfig(Config):
    ENV = 'development'
```

testing

```python
class TestingConfig(Config):
    ENV = 'testing'
```

production

```python
class ProductionConfig(Config):
    ENV = 'production'
```

host

```python
class Config(object):
    HOST = '127.0.0.1'
```

port

```python
class Config(object):
    PORT = 80
```

server name

```python
class Config(object):
    # domain
    SERVER_NAME = 'hallo.com'
```

session

```python
class Config(object):
    # session
    SECRET_KEY = ''
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
```

file upload

```python
class Config(object):
    # file upload
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8M
```

mysql

```python
class Config(object):
    # mysql
    MYSQL_POOL_SIZE = 1
    MYSQL_CONF = dict(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='password',
        database='hallo',
        charset='utf8'
    )
```

redis

```python
class Config(object):
    # redis
    REDIS_URL = 'redis://127.0.0.1:6379/0'
```

memcache

```python
class Config(object):
    # cache
    CACHE_CONF = [
        '127.0.0.1:11211'
    ]
```

oss

```python
class Config(object):
    # oss
    OSS_CONF = dict(
        endpoint='',
        bucket='',
        access_key_id='',
        access_key_secret=''
    )
```

### routing

1、auto routing

```python
http://127.0.0.1/<module>/<controller>/<action>
```

&lt;module&gt;: the directory or subdirectory under module

&lt;controller&gt;: the controller

&lt;action&gt;: the function of controller


2、user defined routing

```python
router = Router(app=app)
router.add('/hello/<name>', 'hello/hi')
```

file: module/hello.py

```python
from app.module.base import BaseController
class HelloController(BaseController):

    def hi(self, name):
        return f'hi, {name}'
```

3、subdomain

file: config.py

```python
class Config(object):
    SERVER_NAME = 'hallo.com'
```

file: router.py

```python
admin = Router(app=app, subdomain='admin', module='admin')
```

### HTTP request

1、get

file: module/http.py
```python
from app.module.base import BaseController

class HttpController(BaseController):
    
    def info(self):
        name = self.get('name')
        age = self.get('age')
        
        return self.ok(dict(
            name=name,
            age=age
        ))
```

2、post

file: module/http.py

```python
from app.module.base import BaseController

class HttpController(BaseController):

    def save(self):
        name = self.post('name')
        age = self.post('age')
        
        return self.ok(dict(
            name=name,
            age=age
        ))
```

3、header

file: module/header.py

```python
from app.module.base import BaseController

class HeaderController(BaseController):

    def token(self):
        token = self.header('Token')
        return self.ok(token)
```

4、file

file: module/file/upload.py

```python
from app.module.base import BaseController

class FileController(BaseController):

    def upload(self):
        file = self.file('file')
```

### mysql

1、add user

file: module/user.py

```python
from app.module.base import BaseController
from app.models.user import User

class UserController(BaseController):

    def add(self):
        username = self.post('username')
        phone = self.post('phone')
        money = self.post('money')
        gender = self.post('gender')

        model = User()
        model.username = username
        model.phone = phone
        model.money = money
        model.gender = gender
        model.save()

        return self.ok()
```

2、edit user

file: module/user.py

```python
from app.module.base import BaseController
from app.models.user import User

class UserController(BaseController):

    def edit(self):
        id = self.post('id')
        username = self.post('username')
        phone = self.post('phone')
        money = self.post('money')
        gender = self.post('gender')

        model = User.find().where(id=id).one()
        if not model:
            return self.error('user not exists')
        model.username = username
        model.phone = phone
        model.money = money
        model.gender = gender
        model.save()

        return self.ok()
```

3、delete user

file: module/user.py

```python
from app.module.base import BaseController
from app.models.user import User

class UserController(BaseController):

    def delete(self):
        id = self.post('id')
        User.find().where(id=id).delete()
        return self.ok()
```

4、list user

file: module/user.py

```python
from app.module.base import BaseController
from app.models.user import User

class UserController(BaseController):

    def list(self):
        self.init_page()
        model = User.find()
        total = model.count()
        all = model.offset(self.offset).limit(self.limit).all(raw=True)
        return self.resp_page(all, total)
```

### redis

1、set

file: module/redis.py

```python
from app.module.base import BaseController

class RedisController(BaseController):

    def mem_set(self):
        try:
            key = self.get('key')
            val = self.get('val')
            self.redis.set(name=key, value=val, ex=3600)
            return self.ok()
        except Exception as e:
            return self.error(str(e))
```

2、get

file: module/redis.py

```python
from app.module.base import BaseController

class RedisController(BaseController):

    def mem_get(self):
        try:
            key = self.get('key')
            val = self.redis.get(key)
            if isinstance(val, bytes):
                return self.ok(val.decode('UTF-8'))
            else:
                return self.error()
        except Exception as e:
            return self.error(str(e))
```

### memcache

1、set

file: module/cache.py

```python
from app.module.base import BaseController

class CacheController(BaseController):

    def mem_set(self):
        key = self.get('key')
        val = self.get('val')
        if self.cache.set(key, val):
            return self.ok()
        else:
            return self.error()
```

2、get

file: module/cache.py

```python
from app.module.base import BaseController

class CacheController(BaseController):

    def mem_get(self):
        key = self.get('key')
        val = self.cache.get(key)
        if val:
            return self.ok(val)
        else:
            return self.error()
```

### file upload

1、local

file: module/file.py

```python
from app.module.base import BaseController
from app.helper.file import File

class FileController(BaseController):

    def upload(self):
        file = self.file('file')
        f = File()
        path = f.upload(file)

        resp = dict()
        resp['path'] = path
        return self.ok(resp)
```

2、oss

file: module/oss.py

```python
from app.module.base import BaseController
from app.helper.oss import Oss

class OssController(BaseController):

    def upload(self):
        file = self.file('file')
        oss = Oss()
        key = oss.upload(file)

        resp = dict()
        resp['key'] = key
        resp['url'] = oss.url(key)
        resp['sign_url'] = oss.sign_url(key=key, expires=3600)
        return self.ok(resp)
```

### template

file: module/html.py

```python
from app.module.base import BaseController

class HtmlController(BaseController):

    def index(self):
        tv = dict()
        tv['title'] = 'hello world!'
        return self.render('html/index.html', tv)
```

### console

1、builtin command: table

file: console/table.py

show all tables

```shell
python console.py table/show
```

create all tables

```shell
python console.py table/build
```

reflect all tables

```shell
python console.py table/model
```

2、builtin command: secret

file: console/secret.py

generate a random secret key

```shell
python console.py secret/key
```

3、user defined command: test

file: console/test.py

```python
from app.console.base import BaseCommand

class TestCommand(BaseCommand):

    def hello(self):
        print('hello')
```

run test command

```shell
python console.py test/hello
```

### log

1、app log

file: log/app.log

```text
2022-07-04 22:12:13 INFO [base.py:28]: flask app init
2022-07-04 22:12:13 INFO [connection_pool.py:36]: put connection into pool
2022-07-04 22:12:13 INFO [_internal.py:224]:  * Running on http://127.0.0.1:80 (Press CTRL+C to quit)
```

2、console log

file: log/console.log

```text
2022-07-04 22:14:33 WARNING [table.py:27]: table user exists
```

log formatter

file: helper/functions.py

```python
def create_log(log_file):
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)s [%(filename)s:%(lineno)s]: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'message': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': log_file,
                'maxBytes': 1024 * 1024,
                'backupCount': 10,
                'encoding': 'utf-8'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi', 'message']
        }
    })
```

### decorator

file: helper/decorator.py

1、time_cost

```python
def time_cost(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        resp = func(*args, **kwargs)
        end = time.time()
        cost = round(end - start, 3)
        logging.info(f'{request.path} time cost={cost}s')
        return resp
    return wrapper
```

2、retry

```python
def retry(num=1, seconds=0):
    def outer(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            for i in range(0, num):
                try:
                    resp = func(*args, **kwargs)
                    if resp['code'] == 0:
                        return resp
                    if seconds > 0:
                        time.sleep(seconds)
                except Exception as e:
                    logging.error(str(e))
            return error(f'retry {num} times and failed')
        return inner
    return outer
```

3、check_login

```python
def check_login(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        userid = session.get('userid')
        if not userid:
            return error('login is required', 401)
        else:
            return func(*args, **kwargs)
    return wrapper
```

4、check_token

```python
def check_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Token')
        if not token:
            return error('token is missing', 401)
        if not app.config['redis'].get(token):
            return error('token is expired', 401)
        else:
            return func(*args, **kwargs)
    return wrapper
```

### Login

1、login by session

file: module/session/user.py

```python
from app.module.base import BaseController
from flask import session
from app.models.user import User
from app.helper.decorator import check_login

class UserController(BaseController):

    def login(self):
        username = self.post('username')
        password = self.post('password')
        user = User.find().where(username=username).one()
        if not user:
            return self.error('user not exists')
        if user.password != password:
            return self.error('wrong password')
        session['userid'] = user.id
        return self.ok('login success')
```

2、logout by session

file: module/session/user.py

```python
from app.module.base import BaseController
from flask import session
from app.models.user import User
from app.helper.decorator import check_login

class UserController(BaseController):

    @check_login
    def logout(self):
        session.pop('userid')
        return self.ok('logout success')
```

3、login by token

file: module/token/user.py

```python
from app.module.base import BaseController
from app.module.user import User
from app.helper.decorator import check_token

class UserController(BaseController):

    def login(self):
        username = self.post('username')
        password = self.post('password')
        user = User.find().where(username=username).one()
        if not user:
            return self.error('user not exists')
        if user.password != password:
            return self.error('wrong password')
        token = user.login()
        resp = dict()
        resp['token'] = token
        return self.ok(resp)
```

4、logout by token

file: module/token/user.py

```python
from app.module.base import BaseController
from app.module.user import User
from app.helper.decorator import check_token

class UserController(BaseController):

    @check_token
    def logout(self):
        self.user.logout()
        return self.ok('logout success')
```

### deploy to production

```shell
cd your-project
hallo install
./install.sh
```

start project

```shell
./supervisor/start.sh
```

stop project

```shell
./supervisor/stop.sh
```

restart project

```shell
./supervisor/restart.sh
```

shutdown project

```shell
./supervisor/shutdown.sh
```

## <a href=#resource>Resource</a>

* Flask: [https://flask.palletsprojects.com/en/2.0.x/](https://flask.palletsprojects.com/en/2.0.x/)
* PyMyORM: [https://github.com/oldjun/PyMyORM](https://github.com/oldjun/PyMyORM)

## <a href=#license>License</a>

Hallo is released under the MIT License. See LICENSE for more information.
