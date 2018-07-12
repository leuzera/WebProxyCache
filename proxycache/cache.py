import logging
from .page import Page, Base
from sqlalchemy import create_engine
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL


class Cache:
    """
    Faz o gerenciamento do cache do proxy.
    """

    def __init__(self):
        url = URL('sqlite', database='database.db')
        engine = create_engine(url)
        session = sessionmaker(bind=engine)
        self.session = session()
        Base.metadata.create_all(engine)

    def is_cached(self, path):
        """
        Retorna verdadeiro, se a pagina está em cache, ou falso, caso contrário.

        :param path: URL
        :return: True caso a página esteja armazenada, False caso contrário.
        """
        (ret,) = self.session.query(exists().where(Page.path == path))
        return ret[0]

    def put_page(self, response):
        """
        Salva a pagina contida em um objeto HTTPResponse.

        :param response: Objeto Response que possui o conteudo de uma pagina web.
        """
        page = Page(response)
        self.session.add(page)
        self.session.commit()
        logging.info(response.url)

    def get_page(self, path):
        """
        Retorna uma pagina armazenada em cache.

        :return: Response.content
        """
        page = self.session.query(Page).filter(Page.path == path).first()
        return page

    def update_page(self, response):
        """
        Atualiza a página em cache para uma mais recente

        :param response: objeto :class::`requests.Response`
        """
        old_page = self.session.query(Page).filter(Page.path == response.url).first()

        old_page.headers = response.headers
        old_page.content = response.content

        self.session.commit()

    def clear_cache(self):
        """
        Limpa o cache

        Apaga todas as páginas salvas

        .. warning::
            Não implementado
        """
        pass
