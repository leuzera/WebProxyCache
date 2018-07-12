from sqlalchemy import Column, String, PickleType, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Page(Base):
    """
    Página em cache.
    SQLAlchemy usa essa classe para criar uma tabela no banco de dados.
    """
    __tablename__ = "pages"

    path = Column(String, primary_key=True)
    page = Column(PickleType)
    counter = Column(Integer)

    def __init__(self, res):
        self.path = res.url
        self.page = res
        self.counter = 1
