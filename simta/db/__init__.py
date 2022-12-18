import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .Base import Base
from .dummies import *
from .dummies import dummies
from . import relationships

db_file = "db.sqlite"

engine = create_engine(f"sqlite+pysqlite:///{db_file}", echo=True, future=True)
Session = sessionmaker(engine)

def init_dummy():
    if os.path.isfile(db_file):
        os.remove(db_file)

    Base.metadata.create_all(engine)

    with Session() as session:
        for x in dummies:
            session.add(x)
        session.commit()
        session.flush()
