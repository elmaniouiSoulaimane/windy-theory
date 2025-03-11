from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base


class Entry(Base):
    __tablename__ = "entries"

    name = Column(String)
    ext = Column(String)
    origin = Column(String)
    destination = Column(String)

    operations = relationship("Operation", back_populates="entry")