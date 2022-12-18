from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
import enum
from sqlalchemy import Enum

from .Base import Base

class MhsLevel(enum.Enum):
    S1 = 1
    S2 = 2
    S3 = 3

class Mahasiswa(Base):
    __tablename__ = "MAHASISWA"

    id = Column("Id", Integer, ForeignKey("USER.Id"), primary_key=True, autoincrement=True)
    nrp = Column("NRP", String(16), nullable=False, unique=True)
    level = Column("Level", Enum(MhsLevel), nullable=False, default=MhsLevel.S1)

