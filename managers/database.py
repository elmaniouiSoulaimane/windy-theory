from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from models import TaskGroup, Task, Operation

Base = declarative_base()

class DatabaseManager:
    _instance = None  # Singleton instance

    def __new__(cls, db_url: str = "sqlite:///history.db"):
        """Initialize the database."""
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.init_db(db_url)
        return cls._instance

    def init_db(self, db_url: str):
        self.engine = create_engine(db_url, echo=False)  # Creates a connection to SQLite database
        self.session_maker = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        self.session = self.session_maker()

        self.create_tables()
        self.seed_data()

    def create_tables(self):
        """Create all tables if they don't exist."""
        Base.metadata.create_all(self.engine)

    def create_session(self) -> Session:
        """Create a new database session."""
        return self.session()
    
    def seed_data(self):
        session = self.create_session()

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

        