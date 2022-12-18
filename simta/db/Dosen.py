from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property

from .Base import Base

class Dosen(Base):
    __tablename__ = "DOSEN"

    id = Column("Id", Integer, ForeignKey("USER.Id"), primary_key=True)
    nip = Column("NIP", String(18), nullable=False, unique=True)
    ttd = Column("Ttd", Boolean, nullable=False, default=False)


