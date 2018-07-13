import logging
import threading
from http.server import HTTPServer
from .proxyhandler import ProxyHandler


class ProxyCache(threading.Thread):
    """
    Configura e inicializa o servidor proxy
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.server_addr = ('', 54321)
        self.httpd = HTTPServer(self.server_addr, ProxyHandler)

    def run(self):
        """Roda para sempre"""
        logging.info("Proxy iniciou em %s" % self.server_addr.__repr__())
        self.httpd.serve_forever()
