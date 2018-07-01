import sqlite3
import requests
import logging


class Cache:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.conn.execute('CREATE TABLE IF NOT EXISTS cache '
                          '(id text primary key not null,'
                          'cacheControl text ,'
                          'expires date ,'
                          'etag text,'
                          'page blob)')
        self.conn.commit()

    def request(self, path):
        res = requests.get(path)
        headers = res.headers

        self.conn.execute("INSERT OR IGNORE INTO cache "
                          "(id, cacheControl, expires, etag, page) VALUES (?,?,?,?,?)",
                          [path,
                           headers.get('Cache-Control'),
                           headers.get('Expires'),
                           headers.get('Etag'),
                           sqlite3.Binary(res.content)])
        self.conn.commit()

        return res
