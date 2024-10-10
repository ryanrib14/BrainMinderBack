from app.db.connection import PostgresDatabaseConfig
from app.config.constants import POSTGRES_URL
from app.db.unitOfWork import UnitOfWork
from sqlalchemy import create_engine
from app.db.repositories.divideRepo import DivideRepository
from typing import Callable, Dict, Any
from sqlalchemy.engine import Engine

if POSTGRES_URL is None:
    raise ValueError("POSTGRES_URL must be set")
# Initialize the DatabaseConfig for the backoffice database
template_database_manager = PostgresDatabaseConfig(database_url=POSTGRES_URL)

# Create the repo_factories dictionary with the correct types
template_repo_factories: Dict[str, Callable[[Any], object]] = {
    "operations_divide_repo": DivideRepository.create
}


def template_get_uow() -> UnitOfWork:
    return UnitOfWork(
        session_factory=template_database_manager.SessionFactory,
        repo_factories=template_repo_factories,
    )


def get_db_engine() -> Engine:
    engine = create_engine(POSTGRES_URL)
    return engine
