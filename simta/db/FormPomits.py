from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Time
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
import enum
from sqlalchemy import Enum

from .Base import Base

class FormPomits(Base):
    __tablename__ = "FORM_POMITS"

    id = Column("Id", Integer, ForeignKey("SIDANG.Id"), primary_key=True)
    check_1 = Column("Check_1", Boolean)
    check_2 = Column("Check_2", Boolean)
    check_3 = Column("Check_3", Boolean)

    @property
    def is_filled(self):
        return self.check_1 is not None \
            and self.check_2 is not None \
            and self.check_3 is not None
