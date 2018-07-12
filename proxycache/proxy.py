import logging
import requests
from datetime import datetime
from .cache import Cache
from http.server import BaseHTTPRequestHandler


class Proxy(BaseHTTPRequestHandler):
    """
    Servidor Proxy

    Recebe as requisições dos clientes e as trata de maneira adequada
    """
    DATE_FORMAT = "%a, %d %b %Y %X %Z"

    def __init__(self, request, client_address, server):
        self.cache = Cache()
        super().__init__(request, client_address, server)

    # noinspection PyPep8Naming
    def do_HEAD(self, page):
        """
        Cria o cabeçalho da resposta HTTP.

        Gera um cabeçalho com código HTTP 200 OK
        Configura o Content-type, Age, Cache-Control e Etag da página

        :param page: objeto de :class:`~proxycache.Page`
        """
        self.send_response(requests.codes.ok)
        self.send_header('Content-type', 'text/html')
        self.send_header('Age', self.age(page))
        self.send_header('Cache-Control', page.headers['Cache-Control'])
        self.send_header('Etag', page.headers['Etag'])
        self.end_headers()

    # noinspection PyPep8Naming
    def do_AUTH_HEAD(self):
        """
        Configura o cabeçalho para resposta com código HTTP 407 Proxy Authentication Required

        """
        self.send_response(requests.codes.proxy_authentication_required)
        self.send_header('Proxy-Authenticate', 'Basic realm=\"Test\"')
        self.end_headers()

    # noinspection PyPep8Naming
    def do_GET(self):
        """
        Processa todas as requisições GET recebidas

        Verifica se pagina está em cache e se é valida

        Envia a pagina em cache ou redireciona a pagina original
        """
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
        """
        Verifica a politica de cache da página

        :param page: objeto de :class:`~proxycache.Page`

        .. warning::
            Não implementado
        """
        pass

    def age(self, page):
        """
        Verifica a idade da página em cache

        :param page: objeto de :class:`~proxycache.Page`
        :return: Idade da página
        """
        page_date = datetime.strptime(page.headers['Expires'], self.DATE_FORMAT)
        return (page_date - datetime.now()).total_seconds()

    def is_fresh(self, page):
        """
        Verifica se a página em cache é fresca

        :param page: objeto de :class:`~proxycache.Page`
        :return:  Boolean
        """
        return self.age(page) > 0

    def is_cacheable(self):
        """
        Verifica a página é passivel de cache

        :return: Boolean

        .. warning::
            Não implementado
        """
        True
