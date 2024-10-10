from app.db.repositories.base import GenericSqlRepository
from app.models.operations.divide import DivideOperation
from typing import List, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.schemas.divide import DivideOperationObject


class DivideRepository(GenericSqlRepository[DivideOperation]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, DivideOperation)

    @classmethod
    def create(cls, session: Session) -> "DivideRepository":
        return cls(session)

    def get_operation_by_id(self, operation_id: int) -> Optional[DivideOperationObject]:
        stmt = text("SELECT * FROM divide_operations WHERE id = :id")
        operation = self._session.execute(stmt, {"id": operation_id}).fetchone()
        if operation:
            return DivideOperationObject.model_construct(**operation._mapping)
        return None

    def list_operations(self) -> Optional[List[DivideOperation]]:
        stmt = text("SELECT * FROM divide_operations")
        operations = self._session.execute(stmt).fetchall()
        return [
            DivideOperationObject.model_construct(**operation._mapping)
            for operation in operations
        ]
