from datetime import datetime
from typing import List, Optional, TypeVar, Type

from sqlalchemy import Column, Integer, inspect, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from managers.database import DatabaseManager

SQLAlchemyBase = declarative_base()

T = TypeVar('T', bound='BaseModel')


class Base(SQLAlchemyBase):
    """Base model class with common CRUD operations."""

    __abstract__ = True  # Tells SQLAlchemy not to create a table for this model

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=None, onupdate=func.now())

    def __repr__(self) -> str:
        """
        Generate a string representation of the model instance.
        Format: ModelName(id=1, attr1=value1, attr2=value2, ...)
        """
        # Get the model class name
        class_name = self.__class__.__name__

        # Get all model attributes excluding relationships
        mapper = inspect(self.__class__)
        attrs = []

        for column in mapper.columns:
            attr_name = column.key
            attr_value = getattr(self, attr_name)

            # Format different types of values appropriately
            if isinstance(attr_value, str):
                formatted_value = f"'{attr_value}'"
            else:
                formatted_value = str(attr_value)

            attrs.append(f"{attr_name}={formatted_value}")

        # Join all attributes into a string
        attrs_str = ", ".join(attrs)
        return f"{class_name}({attrs_str})"

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        """Create a new record if it doesn't exist."""
        # Check if the object already exists
        existing = cls.get(**kwargs)
        if existing:
            return existing

        # Create a new instance
        instance = cls(**kwargs)
        db_manager = DatabaseManager()

        with db_manager.session_scope() as session:
            session.add(instance)
            session.flush()  # Flush to get the ID

        return instance

    @classmethod
    def get(cls: Type[T], **kwargs) -> Optional[T]:
        """Get a record by attributes."""
        # Return None if no filters provided
        if not kwargs:
            return None

        db_manager = DatabaseManager()
        with db_manager.session_scope() as session:
            query = session.query(cls)

            filters_applied = False
            for key, value in kwargs.items():
                if value is not None:
                    query = query.filter(getattr(cls, key) == value)
                    filters_applied = True

            return query.first() if filters_applied else None

    @classmethod
    def get_all(cls: Type[T]) -> List[T]:
        """Get all records."""
        db_manager = DatabaseManager()
        with db_manager.session_scope() as session:
            return session.query(cls).all()

    @classmethod
    def update(cls: Type[T], id: int, **kwargs) -> Optional[T]:
        """Update a record by ID."""
        db_manager = DatabaseManager()
        with db_manager.session_scope() as session:
            instance = session.query(cls).filter(cls.id == id).first()
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
            return instance

    @classmethod
    def delete(cls: Type[T], id: int) -> bool:
        """Delete a record by ID."""
        db_manager = DatabaseManager()
        with db_manager.session_scope() as session:
            instance = session.query(cls).filter(cls.id == id).first()
            if instance:
                session.delete(instance)
                return True
            return False