from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base

class TaskGroup(Base):
    __tablename__ = "task_groups"

    name = Column(String)
    task = relationship("Task", back_populates="task_group")