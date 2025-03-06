import os

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from managers.database import Base
from .entries import Entry
from .users import User
from .tasks import Task

class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())  # Automatically set current timestamp
    keyword = Column(String, nullable=False) # represents the tag or file type to be used for organization

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="operations")

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    task = relationship("Task", back_populates="operations")

    entry_id = Column(Integer, ForeignKey("entries.id"), nullable=False)
    entry = relationship("Entry", back_populates="operations")
    

    def __init__(self, task, entry, user):
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