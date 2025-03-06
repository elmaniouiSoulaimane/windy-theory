from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from managers.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    task_group_id = Column(Integer, ForeignKey("task_groups.id"))
    task_group = relationship("TaskGroup", back_populates="task")

    operations = relationship("Operation", back_populates="task")


    def __init__(self, name, task_group):
        self.name = name
        self.task_group = task_group

    def __repr__(self):
        return f"Task(id={self.id}, name={self.name}, task_group={self.task_group})"