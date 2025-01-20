from sqlalchemy import Column, Integer, String
from .base import Base


class FileTags(Base):
    __tablename__ = "file_tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))