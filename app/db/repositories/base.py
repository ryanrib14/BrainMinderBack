from typing import Type, TypeVar, Generic, List, Optional, Dict, Any
from abc import ABC
from app.db.utils import generate_sql_update_set_args
from sqlalchemy.orm import Session, ColumnProperty
from sqlalchemy import text, inspect
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from uuid import UUID

Base = declarative_base()

T = TypeVar("T", bound=Base)


class GenericSqlRepository(Generic[T], ABC):
    def __init__(self, session: Session, model_cls: Type[T]) -> None:
        self._session = session
        self._model_cls = model_cls

    def get_by_id(self, id: UUID) -> Optional[T]:
        sql = text(
            f"SELECT * FROM {self._model_cls.__table__.schema}.{self._model_cls.__tablename__} WHERE id = :id"
        )
        result = self._session.execute(sql, {"id": id}).fetchone()
        if result:
            return self._model_cls(**result._mapping)
        return None

    def list(self, **filters: Dict[str, Any]) -> List[T]:
        base_sql = f"SELECT * FROM {self._model_cls.__table__.schema}.{self._model_cls.__tablename__}"
        if filters:
            filter_clauses = " AND ".join([f"{key} = :{key}" for key in filters])
            sql = text(f"{base_sql} WHERE {filter_clauses}")
            result = self._session.execute(sql, filters).fetchall()
        else:
            sql = text(base_sql)
            result = self._session.execute(sql).fetchall()
        return result

    def add(self, record: T) -> None:
        mapper = inspect(record.__class__)
        column_attrs = {
            attr.key: getattr(record, attr.key)
            for attr in mapper.attrs
            if isinstance(attr, ColumnProperty)
            and getattr(record, attr.key) is not None
        }
        fields = [key for key in column_attrs if not mapper.columns[key].server_default]
        values = [f":{field}" for field in fields]
        sql_fields = ", ".join(fields)
        sql_values = ", ".join(values)
        sql = text(
            f"INSERT INTO {self._model_cls.__table__.schema}.{self._model_cls.__tablename__} ({sql_fields}) VALUES ({sql_values}) RETURNING id"
        )
        self._session.execute(sql, {field: column_attrs[field] for field in fields})

    def update(self, record: T) -> None:
        assignments = ", ".join(
            [
                f"{field} = :{field}"
                for field in record.__dict__.keys()
                if field in record.__table__.columns
            ]
        )
        sql = text(
            f"UPDATE {self._model_cls.__table__.schema}.{self._model_cls.__tablename__} SET {assignments} WHERE id = :id"
        )
        params = {
            field: getattr(record, field)
            for field in record.__dict__.keys()
            if field in record.__table__.columns
        }
        params["id"] = record.id
        self._session.execute(sql, params)

    def update_object(self, id: UUID, update_data: BaseModel) -> None:
        update_info = update_data.model_dump(exclude_unset=True, exclude_none=True)
        set_string, args = generate_sql_update_set_args(update_info)
        # Add the client_id to the args dictionary
        args["id"] = id
        # Prepare the complete SQL statement for execution
        stmt = text(
            f"UPDATE {self._model_cls.__table__.schema}.{self._model_cls.__tablename__} SET {set_string} WHERE id = :id"
        )
        # Execute the update statement
        self._session.execute(stmt, args)

    def delete(self, id: UUID) -> None:
        sql = text(
            f"DELETE FROM {self._model_cls.__table__.schema}.{self._model_cls.__tablename__} WHERE id = :id"
        )
        self._session.execute(sql, {"id": id})
