import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .Base import Base
from .dummies import *
from .dummies import dummies
from . import relationships
import os

db_file = "assets/db.sqlite"
workdir = os.getenv("WORKDIR", "simta")
db_path = f"{workdir}/{db_file}"

engine = create_engine(f"sqlite+pysqlite:///{db_path}", echo=True, future=True)
Session = sessionmaker(engine)

def init_dummy():

    if os.path.isfile(db_path):
        #os.remove(db_path)
        print("Db already exists")
        return

    Base.metadata.create_all(engine)

    with Session() as session:
        for x in dummies:
            session.add(x)
        session.commit()
        session.flush()
