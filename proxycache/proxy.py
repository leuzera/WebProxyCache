import logging
import requests
from .cache import Cache
from http.server import BaseHTTPRequestHandler


class Proxy(BaseHTTPRequestHandler):
    def do_GET(self):
        cache = Cache('database.db')

        if cache.is_cached(self.path):
            logging.info("Page is cached")
            page = cache.get_page(self.path)
            self.wfile.write(page)
            self.send_response(requests.codes.ok)
        else:
            logging.info("Page is not cached")
            res = requests.get(self.path)
            cache.put_page(res)
            self.wfile.write(res.content)
            self.send_response(res.status_code)
