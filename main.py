import proxycache
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger()

proxy = proxycache.ProxyCache()
flask = proxycache.ProxyStatus()

proxy.start()
flask.start()
