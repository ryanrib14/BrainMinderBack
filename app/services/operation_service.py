from typing import Union
from app.core.operations.divide import Divide
from app.core.base.operation.types import OperationResult


class OperationService:
    """Service for executing operations."""

    @staticmethod
    def divide(a: Union[int, float], b: Union[int, float]) -> OperationResult:
        operation = Divide()
        return operation.execute(a, b)
    
    
