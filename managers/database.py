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
                    cls._instance._init_db(db_url)

        return cls._instance

    def _init_db(self, db_url: str):
        """Initialize database connection and create tables."""
        try:
            self._engine = create_engine(db_url, echo=False)  # Creates a connection to SQLite database
            self._session_maker = sessionmaker(bind=self._engine, autoflush=False, autocommit=False)

            self._create_tables()
            self._seed_data()
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self._session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def _create_tables(self):
        """Create all tables if they don't exist."""
        Base.metadata.create_all(self._engine)

    @staticmethod
    def _seed_task_groups(session) -> None:
        if session.query(TaskGroup).count() == 0:
            session.add_all([
                TaskGroup(name="Organize"),
                TaskGroup(name="Cleanup"),
                TaskGroup(name="Backup"),
                TaskGroup(name="Undo")
            ])

    @staticmethod
    def _seed_tasks(session):
        if session.query(Task).count() == 0:
            org_task_group = session.query(TaskGroup).filter_by(name="Organize").first()
            cln_task_group = session.query(TaskGroup).filter_by(name="Cleanup").first()

            task1 = Task(name="Organize by keyword", task_group=org_task_group)
            task2 = Task(name="Organize by file extension", task_group=org_task_group)
            task3 = Task(name="Remove empty folders", task_group=cln_task_group)
            task4 = Task(name="Empty trash", task_group=cln_task_group)

            session.add_all([task1, task2, task3, task4])
    
    def _seed_data(self):
        try:
            with self.session_scope() as session:
                self._seed_task_groups(session)
                self._seed_tasks(session)
        except Exception as e:
            logger.error(f"Error seeding initial data: {e}")
            raise

        