from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Time, ForeignKeyConstraint, DateTime, UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
import enum
from sqlalchemy import Enum

from .Base import Base

class RevisiStatus(enum.Enum):
    BARU = 1
    DILIHAT = 2
    DITERIMA = 3
    DITOLAK = 4

class Revisi(Base):
    __tablename__ = "REVISI"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    sidang_id = Column("Sidang_Id", Integer, nullable=False)
    penguji_id = Column("Penguji_Id", Integer, nullable=False)
    nomor = Column("Nomor", Integer, default=1, nullable=False)
    status = Column("Status", Enum(RevisiStatus), nullable=False, default=RevisiStatus.BARU)
    created_at = Column("Created_At", DateTime, nullable=False)
    updated_at = Column("Updated_At", DateTime)
    file_name = Column("File_Name", String(32), nullable=False)
    detail = Column("Detail", String(256), nullable=False)

    __table_args__ = (
        UniqueConstraint("Sidang_Id", "Penguji_Id", "Nomor"),
        ForeignKeyConstraint(
            ["Sidang_Id", "Penguji_Id"], ["PENGUJI.Sidang_Id", "PENGUJI.Id"]
        ),
    )
