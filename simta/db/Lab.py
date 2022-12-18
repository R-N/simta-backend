
from sqlalchemy import Column, Integer, String
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property

from .Base import Base

class Lab(Base):
    __tablename__ = "LAB"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    name = Column("Name", String(32), nullable=False)
    short = Column("Short", String(4), nullable=False)

