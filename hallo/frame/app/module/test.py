from app.module.base import BaseController


class TestController(BaseController):

    def hello(self, name):
        return f'hello {name}'
