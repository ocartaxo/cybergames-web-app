import os
import pymysql
import yaml

from models import *


class DatabaseManager:

    def __init__(self):
        self._db = database
        self._configs = None

        root_path = os.path.abspath(os.curdir)
        with open(f'{root_path}/config.yml', mode='r+') as f:
            self._configs = yaml.safe_load(f)['DATABASE']

        self._db_name = self._configs['database']
        self._create_database()

    def _exists_database(self, conn):
        conn.execute("SHOW DATABASES;")
        dbs = [d[0] for d in conn]
        return self._configs['database'] in dbs

    def _create_database(self):
        create_db_info = dict(host=self._configs['host'],
                              user=self._configs['user'],
                              password=self._configs['password'])
        try:
            conn = pymysql.connect(**create_db_info).cursor()
            if not self._exists_database(conn):
                conn.execute(f"CREATE DATABASE {self._db_name};")
                print(f'O banco de dados {self._db_name} foi criado com sucesso')
            conn.close()
        except Exception as e:
            raise e

    def create_tables(self):
        with self._db:
            self._db.create_tables([Jogo, Usuario])

    def init(self):
        self._db.init(**self._configs)

    def connect(self):
        self._db.connect()

    def close(self):
        self._db.close()


if __name__ == "__main__":
    db = DatabaseManager()
    db.init()
