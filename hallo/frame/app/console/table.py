# -*- coding: utf-8 -*-

import os.path
from app.console.base import BaseCommand
from pymyorm.database import Database
import logging


class TableCommand(BaseCommand):

    log_file_name = 'table.log'

    @staticmethod
    def show():
        tables = Database.tables()
        for table in tables:
            logging.info(table)

    def build(self):
        base_path = self.base_path
        sql_path = os.path.join(base_path, 'sql')
        filenames = os.listdir(sql_path)
        for filename in filenames:
            table = filename.split('.')[0]
            exists = Database.exists(table)
            if exists:
                logging.warning(f'table {table} exists')
            else:
                file = os.path.join(self.base_path, 'sql', filename)
                logging.info(f'create table {table}')
                fp = open(file, 'r', encoding='utf-8')
                sql = fp.read()
                try:
                    Database.execute(sql)
                except Exception as e:
                    logging.error(str(e))

    def model(self):
        tables = Database.tables()
        for table in tables:
            model = f'{self.base_path}/app/models/{table}.py'
            if os.path.exists(model):
                logging.warning(f'model {table} exists')
            else:
                logging.info(f'create model {table}')
                Database.reflect(table=table, model=model)


if __name__ == '__main__':
    cmd = TableCommand()
    cmd.build()
