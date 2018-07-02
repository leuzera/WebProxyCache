from sqlalchemy import Column, String, PickleType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Page(Base):
    """Página em cache.
       SQLAlchemy usa essa classe para criar uma tabela no banco de dados."""
    __tablename__ = "pages"

    path = Column(String, primary_key=True)
    cachecontrol = Column(String)
    expires = Column(String)
    etag = Column(String)
    content = Column(PickleType)

    def __init__(self, path, cache, expires, etag, content):
        self.path = path
        self.cachecontrol = cache
        self.expires = expires
        self.etag = etag
        self.content = content
