import logging
import threading

from .proxystatusrouter import app


class ProxyStatus(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.flask = app

    def run(self):
        logging.info("Flask iniciou em ('',54322)")
        self.flask.run(port=54322)
