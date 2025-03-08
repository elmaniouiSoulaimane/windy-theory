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
        Retrieve a Task based on various filters.

        :param id: Optional task ID.
        :param name: Optional task name.
        :param task_group_id: Optional task group ID.
        :return: Task instance or None if no matching task is found.
        """
        db_manager = DatabaseManager()

        with db_manager.session_scope() as session:
            query = session.query(Task)

            if id:
                query = query.filter(Task.id == id)
            if name:
                query = query.filter(Task.name == name)
            if task_group_id:
                query = query.filter(Task.task_group_id == task_group_id)

            return query.first()

    @staticmethod
    def create(
            name: str,
            task_group_id: Optional[int] = None
    ) -> 'Task':
        """
        Create a new Task if it does not already exist.

        :param name: Name of the task (required).
        :param task_group_id: Optional task group ID.
        :return: Existing or newly created Task.
        """
        # Check if a Task with the same name and task_group_id exists
        existing_task = Task.get(name=name, task_group_id=task_group_id)

        if existing_task:
            return existing_task  # Return the existing task

        # Create a new Task instance
        new_task = Task(name=name, task_group_id=task_group_id)

        db_manager = DatabaseManager()

        with db_manager.session_scope() as session:
            session.add(new_task)

            try:
                session.commit()  # Commit the transaction to the database
                return new_task  # Return the newly created task
            except IntegrityError:
                session.rollback()  # Rollback the transaction in case of error
                return session.query(Task).filter_by(name=name, task_group_id=task_group_id).first()