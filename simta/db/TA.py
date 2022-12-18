from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
import enum
from sqlalchemy import Enum

from .Base import Base

class TAType(enum.Enum):
    REQUEST = 1
    PROPOSAL = 2
    TA = 3

class TAStatus(enum.Enum):
    BARU = 1
    BIMBINGAN = 2
    SIDANG = 3
    REVISI = 4
    SELESAI = 5
    DITOLAK = 6

class TA(Base):
    __tablename__ = "TA"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    mhs_id = Column("Mhs_Id", String(16), ForeignKey("MAHASISWA.Id"), nullable=False)
    type = Column("Type", Enum(TAType), nullable=False, default=TAType.REQUEST)
    status = Column("Status", Enum(TAStatus), nullable=False, default=TAStatus.BARU)
    parent_id = Column("Parent_Id", Integer, ForeignKey("TA.Id"))
    judul = Column("Judul", String(64), nullable=False)
