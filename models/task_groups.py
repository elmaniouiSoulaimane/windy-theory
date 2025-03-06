from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from managers.database import Base

class TaskGroup(Base):
    __tablename__ = "task_groups"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    task = relationship("Task", back_populates="task_group")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"TaskGroup(id={self.id}, name={self.name})"