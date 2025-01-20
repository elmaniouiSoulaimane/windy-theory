from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Base, TaskGroup, Task, Operation, Entry, User

class DatabaseManager:
    uri: str = "sqlite:///history.db"
    #engine: create_engine
    #session_factory: sessionmaker

    def __init__(self):
        self.create_tables()
        self.seed_data()
    
    @property
    def con(self) -> create_engine:
        """
        Property to create a database engine using the uri string.
        If the engine does not exist, it is created and stored in the _engine attribute.
        Otherwise, the stored engine is returned.
        """
        if not hasattr(self, "_con"):
            # Creates a connection to SQLite database
            self._con = create_engine(self.uri)
        return self._con

    @property
    def session_maker(self) -> sessionmaker:
        if not hasattr(self, "_session_maker"):
            self._session_maker = sessionmaker(bind=self.con) # Factory for creating sessions
        return self._session_maker
    
    def create_tables(self):
        Base.metadata.create_all(self.con)
    
    def seed_data(self):
        session = self.session_maker()

        try:
            if session.query(TaskGroup).count() == 0:                
                session.add_all(
                    [
                        TaskGroup(name="Organize"), 
                        TaskGroup(name="Cleanup"), 
                        TaskGroup(name="Backup"), 
                        TaskGroup(name="Undo")
                    ]
                )

            if session.query(Task).count() == 0:
                org_task_group = session.query(TaskGroup).filter_by(name="Organize").first()
                cln_task_group = session.query(TaskGroup).filter_by(name="Cleanup").first()

                task1 = Task(name="Organize by a tag/name", task_group=org_task_group)
                task2 = Task(name="Organize by file type/extension", task_group=org_task_group)
                task3 = Task(name="Remove empty folders", task_group=cln_task_group)
                task4 = Task(name="Empty trash", task_group=cln_task_group)
                
                session.add_all([task1, task2, task3, task4])

            session.commit()

        except Exception as e:
            session.rollback()
            print(f"Error seeding data: {e}")

        finally:
            session.close()
    
    @staticmethod
    def create_session() -> Session:
        uri: str = "sqlite:///history.db"
        engine: create_engine = create_engine(uri)
        session: sessionmaker = sessionmaker(bind=engine)

        return session()
