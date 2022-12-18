from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property

from .Base import Base

class User(Base):
    __tablename__ = "USER"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    name = Column("Name", String(64), nullable=False)
    username = Column("Username", String(18), nullable=False, unique=True)
    _password = Column("Password", String(102), nullable=False)
    lab_id = Column("Lab_Id", Integer, ForeignKey("LAB.Id"))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
