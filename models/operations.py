from typing import Optional
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import logging

from managers.database import Base
from .entries import Entry
from .users import User
from .tasks import Task
from typing import Optional

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from managers.database import Base
from .entries import Entry
from .tasks import Task
from .users import User

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
    

    def __init__(self, task, entry, user, keyword: Optional[str] = None, ext: Optional[str] = None):
        if keyword is None and ext is None:
            logger.warning(f"Attempt to insert an operation with keyword and ext values as Null!")

        self.keyword = keyword
        self.ext = ext
        self.task = task
        self.entry = entry
        self.user = user

    def __repr__(self):
        return f"Operation(id={self.id}, created_at={self.created_at}, destination_dir={self.destination_dir}, task_id={self.task_id}, entry_id={self.entry_id}, user_id={self.user_id})"
    
    @staticmethod
    def _create(task: Task, entry: Entry, user: User)-> Operation:
        return Operation(task=task, entry=entry, user=user)
    
    @staticmethod
    def save(entry_name: str, origin: str, destination: str, task: Task, user: User) -> tuple(Entry, Operation):
        entry: Entry = Entry.create(entry_name, origin, destination)
        operation: Operation = Operation._create(task=task, entry=entry, user=user)

        return entry, operation