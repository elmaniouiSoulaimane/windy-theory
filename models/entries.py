from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from managers.database import Base, DatabaseManager
from managers.entry import EntryManager

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    origin = Column(String)
    destination = Column(String)

    operations = relationship("Operation", back_populates="entry")

    def __init__(self, name, type, origin, destination):
        self.name = name
        self.type = type
        self.origin = origin
        self.destination = destination

    def __repr__(self):
        return f"Entry(id={self.id}, name={self.name}, type={self.type}, origin_path={self.origin_path}, new_location={self.new_location})"

    @staticmethod
    def create(name: str, origin: str, destination: str) -> None:
        type_ = EntryManager.get_general_type(name)

        # TODO: what if the database has an entry with the same name?
        new_entry = Entry(name=name, type=type_, origin=origin, destination=destination)
        session = DatabaseManager.create_session()
        session.add(new_entry)
        session.commit()
        session.close()
