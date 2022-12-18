from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
import enum
from sqlalchemy import Enum

from .Base import Base

class PembimbingStatus(enum.Enum):
    PENDING = 1
    BIMBINGAN = 2
    ACC = 3


class Pembimbing(Base):
    __tablename__ = "PEMBIMBING"

    id = Column("Id", Integer, ForeignKey("DOSEN.Id"), primary_key=True)
    ta_id = Column("Ta_Id", Integer, ForeignKey("TA.Id"), primary_key=True)
    nomor = Column("Nomor", Integer, default=1)
    status = Column("Status", Enum(PembimbingStatus), primary_key=True, default=PembimbingStatus.PENDING)


    __table_args__ = (
        UniqueConstraint("Ta_Id", "Nomor"),
    )