import logging
import urllib.request as req
from http.server import BaseHTTPRequestHandler


class Proxy(BaseHTTPRequestHandler):
    def do_GET(self):
        res = req.urlopen(self.path)
        self.wfile.write(res.read())
        self.send_response(res.getcode())
