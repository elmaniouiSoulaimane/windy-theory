from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, TaskGroup, Task, Operation, Entry, User

class DatabaseManager:
    uri: str = "sqlite:///history.db"
    engine: create_engine
    session: sessionmaker

    def __init__(self):
        self.engine = create_engine(self.uri) # lazy initialisation
        self.session = sessionmaker(bind=self.engine) # Factory for creating sessions
        self.create_tables()
        self.seed_data()

    def create_tables(self):
        Base.metadata.create_all(self.engine)
    
    def seed_data(self):
        session = self.session()

        try:
            if session.query(TaskGroup).count() == 0:
                task_group1 = TaskGroup(name="Organize")
                task_group2 = TaskGroup(name="Cleanup")
                task_group3 = TaskGroup(name="Backup")
                task_group4 = TaskGroup(name="Undo")
                
                session.add_all([task_group1, task_group2, task_group3, task_group4])

            if session.query(Task).count() == 0:
                task_group1 = session.query(TaskGroup).filter_by(name="Organize").first()
                task_group2 = session.query(TaskGroup).filter_by(name="Cleanup").first()

                task1 = Task(name="Organize by a tag/name", task_group=task_group1)
                task2 = Task(name="Organize by file type/extension", task_group=task_group1)
                task3 = Task(name="Remove empty folders", task_group=task_group2)
                task4 = Task(name="Empty trash", task_group=task_group2)
                
                session.add_all([task1, task2, task3, task4])

            session.commit()

        except Exception as e:
            session.rollback()
            print(f"Error seeding data: {e}")

        finally:
            session.close()
    
    @staticmethod
    def create_session():
        uri: str = "sqlite:///history.db"
        engine: create_engine = create_engine(uri)
        session: sessionmaker = sessionmaker(bind=engine)

        return session()
