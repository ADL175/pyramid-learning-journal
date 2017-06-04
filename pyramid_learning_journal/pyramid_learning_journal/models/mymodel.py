from sqlalchemy import (
    Column,
    Index,
    Unicode,
    Integer,
    DateTime
)

from .meta import Base


class Journal(Base):
    __tablename__ = 'journal'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    date = Column(DateTime)
    body = Column(Unicode)
