from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Time, ForeignKeyConstraint
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
import enum
from sqlalchemy import Enum

from .Base import Base

class PenolakanRevisi(Base):
    __tablename__ = "PENOLAKAN_REVISI"

    id = Column("Id", Integer, ForeignKey("REVISI.Id"), primary_key=True)
    #sidang_id = Column("Sidang_Id", Integer, primary_key=True)
    #penguji_id = Column("Penguji_Id", Integer, primary_key=True)
    #nomor = Column("Nomor", Integer, default=1, primary_key=True)
    file_name = Column("File_Name", String(32))
    detail = Column("Detail", String(256), nullable=False)

    #__table_args__ = (
    #    ForeignKeyConstraint(
    #        ["Sidang_Id", "Penguji_Id", "Nomor"], ["REVISI.Sidang_Id", "REVISI.Penguji_Id", "REVISI.Nomor"]
    #    ),
    #)
