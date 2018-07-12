import logging

from http.server import HTTPServer

from .proxyhandler import ProxyHandler


class ProxyCache:
    """
    Configura e inicializa o servidor proxy
    """
    def __init__(self, host='', port=54321):
        self.server_addr = (host, port)
        self.httpd = HTTPServer(self.server_addr, ProxyHandler)

    def run(self):
        """Roda para sempre"""
        logging.info("Proxy started at %s" % self.server_addr.__repr__())
        self.httpd.serve_forever()
