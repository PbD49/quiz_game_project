import sqlite3


class DataBase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def execute_query(self, query, params=None):
        if params:
            self.connect()
            self.cursor.execute(query, params)
        else:
            self.connect()
            self.cursor.execute(query)
        self.connection.commit()
        self.disconnect()

    def fetch_all(self, query, params=None):
        if params:
            self.connect()
            self.cursor.execute(query, params)
        else:
            self.connect()
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        if params:
            self.connect()
            self.cursor.execute(query, params)
        else:
            self.connect()
            self.cursor.execute(query)
        return self.cursor.fetchone()


db = DataBase('db.db')
db.connect()