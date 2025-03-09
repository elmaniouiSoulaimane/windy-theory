from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Task(Base):
    __tablename__ = "tasks"

    name = Column(String)
    task_group_id = Column(Integer, ForeignKey("task_groups.id"))
    task_group = relationship("TaskGroup", back_populates="task")
    operations = relationship("Operation", back_populates="task")