import logging
from .page import Page, Base
from sqlalchemy import create_engine
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

class Cache:
    def __init__(self, database):
        url = URL('sqlite', database=database)
        engine = create_engine(url)
        session = sessionmaker(bind=engine)
        self.session = session()
        Base.metadata.create_all(engine)

    def is_cached(self, path):
        (ret, ) = self.session.query(exists().where(Page.path == path))
        return ret[0]

    def put_page(self, response):
        headers = response.headers
        page = Page(response.url,
                    headers.get('Cache-Control'),
                    headers.get('expires'),
                    headers.get('Etag'),
                    response.content)
        self.session.add(page)
        self.session.commit()
        logging.info(response.url, 'cached')

    def get_page(self, path):
        (page,) = self.session.query(Page.content).filter(Page.path == path)
        logging.info('%s recovered from cache', path)
        return page.content

    def clear_cache(self):
        pass

    def is_fresh(self, path):
        pass

    def page_age(self, path):
        pass

