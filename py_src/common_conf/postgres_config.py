from sqlalchemy import create_engine



import psycopg2

class PostgresConfig():
    def __init__(self):
        self.host = '172.18.78.165'
        self.port = 5432
        self.user = 'dash_svc'
        self.passwd = '!dash_svc'
        self.db = 'dash'
        self.set_conn()
        self.engine = create_engine(f'postgresql://{self.user}:{self.passwd}@{self.host}:5432/{self.db}')

    def set_conn(self):
        self.conn = psycopg2.connect(
            host=self.host,
            dbname='dash',
            user=self.user,
            password=self.passwd)
        self.cur = self.conn.cursor()

