import logging
import requests
from datetime import datetime
from .cache import Cache
from http.server import BaseHTTPRequestHandler


class Proxy(BaseHTTPRequestHandler):
    DATE_FORMAT = "%a, %d %b %Y %X %Z"

    def __init__(self, request, client_address, server):
        self.cache = Cache()
        super().__init__(request, client_address, server)

    # noinspection PyPep8Naming
    def do_HEAD(self, page):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Age', self.age(page))
        self.send_header('Cache-Control', page.cachecontrol)
        self.send_header('Etag', page.etag)
        self.end_headers()

    # noinspection PyPep8Naming
    def do_AUTH_HEAD(self):
        self.send_response(407)
        self.send_header('Proxy-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # noinspection PyPep8Naming
    def do_GET(self):
        if self.cache.is_cached(self.path):
            page = self.cache.get_page(self.path)
            if not self.is_fresh(page):
                page = requests.get(self.path, headers={"If-None-Match": page.etag})
                if page.status_code == requests.codes.ok:
                    logging.info("Got new page")
                    self.cache.update_page(page)
        else:
            page = requests.get(self.path)
            self.cache.put_page(page)

        self.protocol_version = 'HTTP/1.1'
        self.do_HEAD(page)
        self.wfile.write(page.content)

    def cache_policy(self, page):
        pass

    def age(self, page):
        page_date = datetime.strptime(page.expires, self.DATE_FORMAT)
        return (page_date - datetime.now()).total_seconds()

    def is_fresh(self, page):
        return self.age(page) > 0

    def is_cacheable(self):
        True
