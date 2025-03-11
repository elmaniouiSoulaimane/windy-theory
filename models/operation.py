import logging

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base

logger = logging.getLogger(__name__)


class Operation(Base):
    __tablename__ = "Operation"

    keyword = Column(String, nullable=True)
    ext = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    user = relationship("User", back_populates="operation")

    task_id = Column(Integer, ForeignKey("Task.id"), nullable=False)
    task = relationship("Task", back_populates="operation")

    entry_id = Column(Integer, ForeignKey("Entry.id"), nullable=False)
    entry = relationship("Entry", back_populates="operation")