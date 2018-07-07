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
    def do_GET(self):
        if self.cache.is_cached(self.path):
            page = self.cache.get_page(self.path)
            if not self.is_fresh(self.path):
                page = requests.get(self.path, headers={"If-None-Match": page.etag})
                if page.status_code == requests.codes.ok:
                    logging.info("Got new page")
                    self.cache.update_page(page)
        else:
            page = requests.get(self.path)
            self.cache.put_page(page)

        self.wfile.write(page.content)
        self.send_response(requests.codes.ok)

    def cache_policy(self, page):
        pass

    def is_fresh(self, path):
        headers = self.cache.get_headers(path)
        page_date = datetime.strptime(headers[1], self.DATE_FORMAT)

        age = (page_date - datetime.now()).total_seconds()

        return age > 0
