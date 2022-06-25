# -*- coding: utf-8 -*-

from app.base import app


if __name__ == '__main__':
    app.run(debug=False, host=app.config['HOST'], port=app.config['PORT'])
