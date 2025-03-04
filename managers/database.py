from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Base, TaskGroup, Task, Operation


class DatabaseManager:
    def __init__(self, db_url: str = "sqlite:///history.db"):
        """Initialize the database connection."""
        self.engine = create_engine(db_url, echo=False) # Creates a connection to SQLite database
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        self.create_tables()
        self.seed_data()
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()

    def close_session(self, session: Session):
        """Close the given session."""
        session.close()
    
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

    @staticmethod
    def save(org_type: str, entry_name: str, origin:str, destination: str):
        db_session = DatabaseManager.create_session()

        try:
            # user_name = os.environ.get('USER')
            # user: User = db_session.query(User).filter_by(name=user_name).first()
            # task: Task = db_session.query(Task).filter_by(name=org_type).first()

            # if not entry or not user or not task:
            #     print(f"Missing required data: entry={entry}, user={user}, task={task}")
            #     return
            
            Operation.create()
            db_session.add_all([entry, operation])
            db_session.commit()

        except Exception as e:
            db_session.rollback()
            print(f"Error saving record: {e}")

        finally:
            db_session.close()

        