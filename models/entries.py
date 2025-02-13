from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from managers.entry import EntryManager

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    origin = Column(String)
    destination = Column(String)

    operations = relationship("Operation", back_populates="entry")

    def __init__(self, name, type, origin_path, new_location):
        self.name = name
        self.type = type
        self.origin_path = origin_path
        self.new_location = new_location

    def __repr__(self):
        return f"Entry(id={self.id}, name={self.name}, type={self.type}, origin_path={self.origin_path}, new_location={self.new_location})"

    @staticmethod
    def create(name: str, origin: str, destination: str) -> Entry:
        type_ = EntryManager.get_general_type(name)

        # TODO: what if the database has an entry with the same name?
        return Entry(name=name, type=type_, origin=origin, destination=destination)
