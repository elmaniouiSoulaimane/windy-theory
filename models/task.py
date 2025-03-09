from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from managers.database import Base, DatabaseManager

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    task_group_id = Column(Integer, ForeignKey("task_groups.id"))
    task_group = relationship("TaskGroup", back_populates="task")

    operations = relationship("Operation", back_populates="task")

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, task_group={self.task_group})>"

    @staticmethod
    def get(
            id: Optional[int] = None,
            name: Optional[str] = None,
            task_group_id: Optional[int] = None
    ) -> Optional['Task']:
        """
        Retrieves a Task object from the database, given certain criteria.

        Retrieves a Task object from the database, given an ID, name, or task group ID.
        This method takes in any combination of the following parameters, and
        returns a Task object that matches all of the given criteria. If no
        matching Task object is found, it returns None.

        Parameters:
            id (Optional[int]): The ID of the Task object to retrieve.
            name (Optional[str]): The name of the Task object to retrieve.
            task_group_id (Optional[int]): The ID of the TaskGroup that the Task
                object to retrieve belongs to.

        Returns:
            Optional[Task]: The retrieved Task object, or None if no matching
                Task object was found.
        """
        db_manager = DatabaseManager()

        with db_manager.session_scope() as session:
            query = session.query(Task)

            filters_applied = False

            if id is not None:
                query = query.filter(Task.id == id)
                filters_applied = True
            if name is not None:
                query = query.filter(Task.name == name)
                filters_applied = True
            if task_group_id is not None:
                query = query.filter(Task.task_group_id == task_group_id)
                filters_applied = True

            return query.first() if filters_applied else None

    @staticmethod
    def create(
            name: str,
            task_group_id: Optional[int] = None
    ) -> 'Task':
        """
        Creates a new Task object, given a name and optional task group ID.

        Creates a new Task object with the given name and task group ID. If
        a Task object with the same name already exists in the database,
        it simply returns the existing object. Otherwise, it creates a new
        Task object, adds it to the database, and then returns the new
        Task object.

        Parameters:
            name (str): The name of the Task object to create.
            task_group_id (Optional[int]): The ID of the TaskGroup that the new
                Task object should belong to.

        Returns:
            Task: The newly created Task object, or the existing Task object
                if one already exists with the given name.
        """
        existing_task = Task.get(name=name)

        if existing_task:
            return existing_task

        new_task = Task(name=name, task_group_id=task_group_id)

        db_manager = DatabaseManager()

        with db_manager.session_scope() as session:
            session.add(new_task)
            session.flush()
            return new_task