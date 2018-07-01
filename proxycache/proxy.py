import logging
from .cache import Cache

from http.server import BaseHTTPRequestHandler


class Proxy(BaseHTTPRequestHandler):
    def do_GET(self):
        res = Cache().request(self.path)
        self.wfile.write(res.content)
        self.send_response(res.status_code)
