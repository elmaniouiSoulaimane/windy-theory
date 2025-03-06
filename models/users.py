from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from managers.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    operations = relationship("Operation", back_populates="user")


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"