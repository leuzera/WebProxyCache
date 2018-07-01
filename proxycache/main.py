import logging

from http.server import HTTPServer

from .proxy import Proxy


class ProxyCache:
    def __init__(self, host='', port=54321):
        self.server_addr = (host, port)
        self.httpd = HTTPServer(self.server_addr, Proxy)
        logging.log(logging.INFO, "Proxy running")

    def run(self):
        self.httpd.serve_forever()
