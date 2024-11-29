import mysql.connector

from repositories.repository_exception import RepositoryException


class BaseRepository:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='scraping'
        )
        self.cursor = self.conn.cursor()
        self._complete = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def complete(self):
        self._complete = True

    def close(self):
        if self.conn.is_connected():
            try:
                if self._complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                self.conn.rollback()
                raise RepositoryException(*e.args)
            finally:
                self.cursor.close()
                self.conn.close()

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor

    def execute_many(self, query, params=None):
        if params is None:
            params = []
        self.cursor.executemany(query, params)
        return self.cursor
