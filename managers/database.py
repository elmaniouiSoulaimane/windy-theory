import logging
from contextlib import contextmanager
from threading import Lock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from models import TaskGroup, Task

Base = declarative_base()
logger = logging.getLogger(__name__)

class DatabaseManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, db_url: str = "sqlite:///history.db"):
        if not cls._instance:
            with cls._lock:
                # Double-checked locking
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance.init_db(db_url)

        return cls._instance

    def init_db(self, db_url: str):
        """Initialize database connection and create tables."""
        try:
            self.engine = create_engine(db_url, echo=False)  # Creates a connection to SQLite database
            self.session_maker = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

            self.create_tables()
            self.seed_data()
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_tables(self):
        """Create all tables if they don't exist."""
        Base.metadata.create_all(self.engine)
    
    def seed_data(self):
        with self.session_scope() as session:
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

        