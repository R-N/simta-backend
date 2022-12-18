from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
import enum
from sqlalchemy import Enum

from .Base import Base

class PengujiStatus(enum.Enum):
    PENDING = 1
    MENGUJI = 2
    ACC = 3


class Penguji(Base):
    __tablename__ = "PENGUJI"

    id = Column("Id", Integer, ForeignKey("DOSEN.Id"), primary_key=True)
    sidang_id = Column("Sidang_Id", Integer, ForeignKey("SIDANG.Id"), primary_key=True)
    nomor = Column("Nomor", Integer, default=1)
    status = Column("Status", Enum(PengujiStatus), default=PengujiStatus.PENDING)
    catatan_revisi = Column("Catatan_Revisi", String(256))
    nilai = Column("Nilai", Integer)

    __table_args__ = (
        UniqueConstraint("Sidang_Id", "Nomor"),
    )
