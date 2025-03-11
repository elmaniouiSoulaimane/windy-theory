from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "User"

    name = Column(String)
    operations = relationship("Operation", back_populates="user")