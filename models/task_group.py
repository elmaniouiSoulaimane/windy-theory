from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base


class TaskGroup(Base):
    __tablename__ = "task_group"

    name = Column(String)
    task = relationship("Task", back_populates="task_group")