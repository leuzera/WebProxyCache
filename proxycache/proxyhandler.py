import logging
import requests
from datetime import datetime, timedelta
from .cache import Cache
from http.server import BaseHTTPRequestHandler


class ProxyHandler(BaseHTTPRequestHandler):
    """
    Servidor Proxy

    Recebe as requisições dos clientes e as trata de maneira adequada
    """
    DATE_FORMAT = "%a, %d %b %Y %X %Z"

    def __init__(self, request, client_address, server):
        self.cache = Cache()
        self.page = None
        super().__init__(request, client_address, server)

    # noinspection PyPep8Naming
    def do_HEAD(self):
        """
        Cria o cabeçalho da resposta HTTP.

        Gera um cabeçalho com código HTTP 200 OK
        Configura o Content-type, Age, Cache-Control e Etag da página
        """
        self.send_response(requests.codes.ok)

        if self.page.headers.get('Content-type'):
            self.send_header('Content-type', self.page.headers.get('Content-type'))
        if self.page.headers.get('Cache-Control'):
            self.send_header('Cache-Control', self.page.headers.get('Cache-Control'))
        if self.page.headers.get('Etag'):
            self.send_header('Etag', self.page.headers.get('Etag'))

        self.send_header('Age', self._age())
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
        logging.debug("{}".format(self.path))
        if self.cache.is_cached(self.path):
            """Se a pagina estiver em cache, recuperamos ela"""
            logging.info("Pagina em cache")
            self.page = self.cache.get_page(self.path)
            if not self._is_fresh():
                """Se ela não for fresca, verificamos se foi modificada"""
                logging.debug("")
                if self.page.headers.get('Etag'):
                    compare = {"If-None-Match": self.page.headers.get('Etag')}
                elif self.page.headers.get('Last-Modified'):
                    compare = {"If-Modified-Since": self.page.headers.get('Last-Modified')}
                else:
                    compare = {}

                _page = requests.get(self.path, headers=compare)

                logging.info("Validando página")
                logging.debug("Status:{}\tHeaders:{}".format(_page.status_code,compare))
                if _page.status_code == requests.codes.ok:
                    """Se foi modificada, atualizamos a página em cache"""
                    self.page = _page
                    self.cache.update_page(self.page)
        else:
            """Se a pagina não estiver em cache, baixamos ela"""
            logging.info("Página fora do cache")
            self.page = requests.get(self.path)
            if self._is_cacheable():
                """Se ela permitir ser guardade em cache, salvamos ela"""
                self.cache.put_page(self.page)

        self.protocol_version = 'HTTP/1.1'
        self.do_HEAD()
        self.wfile.write(self.page.content)

    def do_POST(self):
        requests.post(self.path)

    def do_PUT(self):
        requests.put(self.path)

    def do_DELETE(self):
        requests.delete(self.path)

    def do_OPTIONS(self):
        requests.options(self.path)

    def _cache_policy(self):
        """
        Verifica a politica de cache da página

        :return: As politicas de cache da página ou None
        """
        policy = self.page.headers.get("Cache-Control")
        if policy is None:
            return None
        else:
            return policy.split(',')

    def _age(self):
        """
        Verifica a idade da página em cache

        :return: Idade da página em segundos
        """
        date = self.page.headers.get('Date')
        page_date = datetime.strptime(date, self.DATE_FORMAT)

        return (page_date - datetime.now()).total_seconds()

    def _is_fresh(self):
        """
        Verifica se a página em cache é fresca

        :return:  Se é fresca (Boolean)
        """
        current_age = timedelta(seconds=self._age())
        response_time = datetime.strptime(self.page.headers.get('Date'), self.DATE_FORMAT)

        if self.page.headers.get('Expires'):
            freshness_lifetime = datetime.strptime(self.page.headers.get('Expires'), self.DATE_FORMAT) - response_time
        else:
            freshness_lifetime = self._max_age()

        return (freshness_lifetime - current_age) > timedelta(seconds=0)

    def _is_cacheable(self):
        """
        Verifica a página é passivel de cache

        :return: Se é possivel armazenas em cache (Boolean)

        .. note::
            Caso ``Cache-Control`` tenha ``no-cache``  a página não deve ser mantida em cache
        """
        policy = self._cache_policy()
        if policy is None or 'no-cache' not in policy:
            return True
        else:
            return False

    def _max_age(self):
        """
        Retorna a idade máxima da página

        :return: Idade maxima da página em :class:`datetime.timedelta`
        """
        max_age = [age for age in self.page.headers if age.startwith('max-age=')]
        return timedelta(seconds=max_age[0].strip('max-age='))
