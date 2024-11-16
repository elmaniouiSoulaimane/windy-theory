from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    origin_path = Column(String)

    operations = relationship("Operation", back_populates="entry")

    def __init__(self, name, type, origin_path):
        self.name = name
        self.type = type
        self.origin_path = origin_path

    def __repr__(self):
        return f"Entry(id={self.id}, name={self.name}, type={self.type}, origin_path={self.origin_path})"
