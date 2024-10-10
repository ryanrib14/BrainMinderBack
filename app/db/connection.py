from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, text, Engine
from typing import Callable


class PostgresDatabaseConfig:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = self.create_engine()
        self.SessionFactory = self.create_session_factory()

    def create_engine(self) -> Engine:
        return create_engine(self.database_url)

    def create_session_factory(self) -> sessionmaker:
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


def get_session(database_manager: PostgresDatabaseConfig) -> Session:  # type: ignore
    db = database_manager.SessionFactory()
    try:
        yield db
    finally:
        db.close()


def create_sqlalchemy_engine(database_url: str) -> Engine:
    engine = create_engine(database_url)
    return engine


def get_sqlalchemy_session(engine: Engine) -> Callable[[], Session]:
    Session = sessionmaker(autocommit=False, bind=engine, autoflush=False)
    return lambda: Session()


def terminate_active_connections(engine: Engine, template_db: str) -> None:
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        terminate_stmt = text(
            f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{template_db}'
            AND pid <> pg_backend_pid();
        """
        )
        conn.execute(terminate_stmt)
