from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    name = Column(String)
    operations = relationship("Operation", back_populates="user")