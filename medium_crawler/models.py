"""Database ORM models."""
import os
from os.path import abspath, dirname, join

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def db_connect():
    """Database connection."""
    PROJ_ROOT = dirname(dirname(abspath(__file__)))
    SQLITE_PATH = join(PROJ_ROOT, 'rule.db')
    URI = f'sqlite:///{SQLITE_PATH}'
    return create_engine(os.environ.get('DATABASE_URL', URI))


def create_new_table(engine):
    """Create all tables that do not already exist."""
    Base.metadata.create_all(engine)


class Rule(Base):
    """Table for spider arguments."""

    __tablename__ = 'rule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30))
    date = Column(String(8))
    back = Column(Integer)
    url = Column(String)
    source = Column(String(30))
    enable = Column(Integer)
