from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from typing import Optional
from managers.database import Base, DatabaseManager

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    operations = relationship("Operation", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"

    @staticmethod
    def get(id: Optional[int] = None, name: Optional[str] = None) -> Optional['User']:
        """
        Retrieve a User by their ID or name.

        If both the ID and name are `None`, `None` is returned.

        :param id: The ID of the user to retrieve.
        :param name: The name of the user to retrieve.
        :return: The retrieved User, or `None`.
        """
        db_manager = DatabaseManager()

        with db_manager.session_scope() as session:
            query = session.query(User)

            filters_applied = False

            if id is not None:
                query = query.filter(User.id == id)
                filters_applied = True
            if name is not None:
                query = query.filter(User.name == name)
                filters_applied = True

            return query.first() if filters_applied else None

    @staticmethod
    def create(name: str) -> 'User':
        """
        Create a new User or retrieve an existing one by name.

        This method checks if a User with the given name already exists.
        If so, it returns the existing User. Otherwise, it creates a
        new User with the specified name, adds it to the database, and
        returns the newly created User.

        :param name: The name of the User to create or retrieve.
        :return: The existing or newly created User.
        """
        existing_user = User.get(name=name)

        if existing_user:
            return existing_user

        new_user = User(name=name)

        db_manager = DatabaseManager()

        with db_manager.session_scope() as session:
            session.add(new_user)
            session.flush()
            return new_user