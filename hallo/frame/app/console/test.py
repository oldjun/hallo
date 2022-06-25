from app.console.base import BaseCommand


class TestCommand(BaseCommand):

    def hello(self):
        print('test/hello')


if __name__ == '__main__':
    cmd = TestCommand()
    cmd.hello()
