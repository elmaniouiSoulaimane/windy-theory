import logging
from typing import Optional

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from managers.database import Base
from managers.database import DatabaseManager

logger = logging.getLogger(__name__)


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())  # Automatically set current timestamp
    keyword = Column(String, nullable=True)
    ext = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="operations")

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    task = relationship("Task", back_populates="operations")

    entry_id = Column(Integer, ForeignKey("entries.id"), nullable=False)
    entry = relationship("Entry", back_populates="operations")

    def __repr__(self):
        return f"<Operation(id={self.id}, created_at={self.created_at}, keyword={self.keyword}, ext={self.ext}, task_id={self.task_id}, entry_id={self.entry_id}, user_id={self.user_id})>"

    @staticmethod
    def get(id: Optional[int] = None, keyword: Optional[str] = None, ext: Optional[str] = None, user_id: Optional[int] = None, task_id: Optional[int] = None, entry_id: Optional[int] = None) -> Optional['Operation']:
        """
        Retrieves an Operation from the database.

        This method takes in a series of filters, and returns the first matching
        Operation. If no filters are provided, all Operations are returned.

        :param id: The ID of the operation to retrieve. If provided, the other
            parameters are ignored.
        :type id: int
        :param keyword: The keyword associated with the operation.
        :type keyword: str
        :param ext: The extension associated with the operation.
        :type ext: str
        :param user_id: The ID of the user associated with the operation.
        :type user_id: int
        :param task_id: The ID of the task associated with the operation.
        :type task_id: int
        :param entry_id: The ID of the entry associated with the operation.
        :type entry_id: int
        :return: The matching Operation, or None if no match is found.
        :rtype: Operation
        """
        db_manager = DatabaseManager()

        with db_manager.session_scope() as session:
            query = session.query(Operation)

            filters_applied = False

            if id is not None:
                query = query.filter(Operation.id == id)
                filters_applied = True
            if keyword is not None:
                query = query.filter(Operation.keyword == keyword)
                filters_applied = True
            if ext is not None:
                query = query.filter(Operation.ext == ext)
                filters_applied = True
            if user_id is not None:
                query = query.filter(Operation.user_id == user_id)
                filters_applied = True
            if task_id is not None:
                query = query.filter(Operation.task_id == task_id)
                filters_applied = True
            if entry_id is not None:
                query = query.filter(Operation.entry_id == entry_id)
                filters_applied = True

            return query.first() if filters_applied else None

    @staticmethod
    def create(keyword: Optional[str], ext: Optional[str], user_id: Optional[int], task_id: Optional[int], entry_id: Optional[int]) -> 'Operation':
        """
        Creates a new Operation in the database.

        This method takes in a series of optional parameters, and creates a new
        Operation if one does not already exist. If an Operation with the same
        parameters already exists, the existing Operation is returned instead.

        :param keyword: The keyword associated with the operation.
        :type keyword: str
        :param ext: The extension associated with the operation.
        :type ext: str
        :param user_id: The ID of the user associated with the operation.
        :type user_id: int
        :param task_id: The ID of the task associated with the operation.
        :type task_id: int
        :param entry_id: The ID of the entry associated with the operation.
        :type entry_id: int
        :return: The newly created Operation, or the existing Operation if it already exists.
        :rtype: Operation
        """
        existing_operation = Operation.get(keyword=keyword, ext=ext, user_id=user_id, task_id=task_id, entry_id=entry_id)

        if existing_operation:
            return existing_operation

        if not keyword and not ext:
            logger.warning("About to create an Operation without a keyword or ext value!")
        new_operation = Operation(keyword=keyword, ext=ext, user_id=user_id, task_id=task_id, entry_id=entry_id)

        db_manager = DatabaseManager()

        with db_manager.session_scope() as session:
            session.add(new_operation)
            session.flush()
            return new_operation
