import logging

from http.server import HTTPServer

from .proxy import Proxy


class ProxyCache:
    """
    Configura e inicializa o servidor proxy
    """
    def __init__(self, host='', port=54321):
        logging.basicConfig(filename="proxy.log", level=logging.INFO)
        self.server_addr = (host, port)
        self.httpd = HTTPServer(self.server_addr, Proxy)

    def run(self):
        """Roda para sempre"""
        logging.info("Proxy started at %s" % self.server_addr.__repr__())
        self.httpd.serve_forever()
