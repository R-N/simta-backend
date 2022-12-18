from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Time
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
import enum
from sqlalchemy import Enum

from .Base import Base

class SidangStatus(enum.Enum):
    BARU = 1
    FIX = 2
    SELESAI = 3
    LULUS = 4
    MENGULANG = 5

class Sidang(Base):
    __tablename__ = "SIDANG"

    id = Column("Id", Integer, ForeignKey("TA.Id"), primary_key=True)
    date = Column("Date", Date, nullable=False)
    start = Column("Start", Time, nullable=False)
    end = Column("End", Time, nullable=False)
    status = Column("Status", Enum(SidangStatus), nullable=False, default=SidangStatus.BARU)
