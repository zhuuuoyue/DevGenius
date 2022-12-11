# coding: utf-8

import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker


_db_path = f"{os.getcwd()}\\data.db"
_engine = create_engine(f"sqlite:///{_db_path}")
Session = sessionmaker(bind=_engine)
Base = declarative_base()
_session = Session()


class Repository(Base):

    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    path = Column(String(1024), nullable=False)


class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(1024), nullable=False)
    url = Column(String(1024))


class Archive(Base):

    __tablename__ = "archives"

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    path = Column(String(1024), nullable=False)
    md5 = Column(String(255), nullable=False)


class RelTaskArchive(Base):

    __tablename__ = "rel_task_archive"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    archive_id = Column(Integer, ForeignKey("archives.id"))


def create_tables_if_not_exist():
    if not os.path.isfile(_db_path):
        global _engine
        Base.metadata.create_all(_engine)


def get_session():
    global _session
    return _session
