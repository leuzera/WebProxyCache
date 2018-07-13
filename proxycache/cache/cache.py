import logging
from .page import Page, Base
from sqlalchemy import create_engine, func
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
        (ret,) = self.session.query(exists().where(Page.path == path)).first()
        logging.debug("Cached: {}".format(ret))
        return ret

    def put_page(self, response):
        """
        Salva a pagina contida em um objeto HTTPResponse.

        :param response: Objeto Response que possui o conteudo de uma pagina web.
        """
        page = Page(response)
        self.session.add(page)
        self.session.commit()
        logging.debug("{} salva".format(response.url))

    def get_page(self, path):
        """
        Retorna uma pagina armazenada em cache.

        :return: Objeto :class:`requests.Response`
        """
        page = self.session.query(Page).filter(Page.path == path).first()
        logging.debug("{} recuperada".format(path))
        self.session.query(Page).filter(Page.path == path).update({'counter': Page.counter+1})
        return page.page

    def update_page(self, response):
        """
        Atualiza a página em cache para uma mais recente

        :param response: objeto :class:`requests.Response`
        """
        self.session.query(Page).filter(Page.path == response.url).update({'page': response})
        logging.debug("{} atualizada".format(response.url))

    def delete_page(self, path):
        """
        Apaga uma página

        :param path: URL da pagina a ser apagada
        """
        page = self.session.query(Page).filter(Page.path == path).first()
        self.session.delete(page)
        logging.debug("{} apagada".format(path))

    def get_pages_top(self):
        return self.session.query(Page).all()

    def get_pages_num(self):
        return self.session.query(func.count(Page.path)).first()[0]
