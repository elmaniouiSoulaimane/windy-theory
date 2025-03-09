from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from typing import Optional
from managers.database import Base, DatabaseManager

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    ext = Column(String)
    origin = Column(String)
    destination = Column(String)

    operations = relationship("Operation", back_populates="entry")

    def __repr__(self):
        return f"<Entry(id={self.id}, name={self.name}, ext={self.ext}, origin={self.origin}, destination={self.destination})>"

    @staticmethod
    def get(id: Optional[int] = None, name: Optional[str] = None, ext: Optional[str] = None, origin: Optional[str] = None,
            destination: Optional[str] = None) -> Optional['Entry']:
        """
        Retrieves an Entry from the database based on the given parameters.

        :param id: ID of the Entry to retrieve.
        :param name: Name of the Entry to retrieve.
        :param ext: Extension of the Entry to retrieve.
        :param origin: Origin path of the Entry to retrieve.
        :param destination: Destination path of the Entry to retrieve.
        :return: An Entry object if found, None otherwise.
        """
        db_manager = DatabaseManager()
        with db_manager.session_scope() as session:
            query = session.query(Entry)

            filters_applied = False

            if id is not None:
                query = query.filter(Entry.id == id)
                filters_applied = True
            if name is not None:
                query = query.filter(Entry.name == name)
                filters_applied = True
            if ext is not None:
                query = query.filter(Entry.ext == ext)
                filters_applied = True
            if origin is not None:
                query = query.filter(Entry.origin == origin)
                filters_applied = True
            if destination is not None:
                query = query.filter(Entry.destination == destination)
                filters_applied = True

            return query.first()

    @staticmethod
    def create(name: str, ext: str, origin: str, destination: str) -> 'Entry':
        """
        Creates a new Entry in the database if it does not already exist.

        :param name: Name of the Entry to create.
        :param ext: Extension of the Entry to create.
        :param origin: Origin path of the Entry to create.
        :param destination: Destination path of the Entry to create.
        :return: The newly created Entry if it did not already exist, the existing Entry if it did.
        """
        existing_entry = Entry.get(name=name, ext=ext, origin=origin, destination=destination)

        if existing_entry:
            return existing_entry

        new_entry = Entry(name=name, ext=ext, origin=origin, destination=destination)
        db_manager = DatabaseManager()

        with db_manager.session_scope() as session:
            session.add(new_entry)
            session.flush()
            return new_entry