import datetime
import psycopg2
import os
import json
import pytz
from pathlib import Path

source_path = Path(__file__).resolve()
source_dir = source_path.parent


def get_utc_now():
    return str(int(datetime.datetime.now(tz=pytz.utc).timestamp() * 1000))


class SqlDatabase:
    def __init__(self):
        self.cur = None
        self.conn = None
        path = os.path.join(source_dir, 'config.json')
        with open(path, 'r') as f:
            credentials = json.load(f)
        self.config = {
            "filter_host": credentials["filter_host"],
            "filter_port": credentials["filter_port"],
            "db_host": credentials["db_host"],
            "dbname": credentials["dbname"],
            "user": credentials["user"],
            "password": credentials["password"],
            "unsplash_access_key": credentials["unsplash_access_key"]
        }
        self.connect()

    def connect(self):
        self.conn = psycopg2.connect(
            f'dbname={self.config["dbname"]} '
            f'user={self.config["user"]} '
            f'host={self.config["db_host"]} '
            f'password={self.config["password"]}')
        self.cur = self.conn.cursor()
        return None

    def commit(self):
        self.cur.close()
        self.conn.commit()
        self.connect()
        return None

    def fetch_n_image_arrs(self, n):
        try:
            sql_syntax = 'SELECT image_arr FROM image_table limit ' + str(n) + ';'
            self.cur.execute(sql_syntax)
            data = self.cur.fetchall()
            self.commit()
        except Exception as e:
            print("fetch_image_data", e)
            curs = self.conn.cursor()
            curs.execute("ROLLBACK")
            self.commit()
            data = list()
        return data
