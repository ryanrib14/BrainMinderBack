from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    """Enumeration of available operation types."""

    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"


class Operand(BaseModel):
    """Model for an operand."""

    value: float

    def __str__(self) -> str:
        return str(self.value)


class OperationResult(BaseModel):
    """Model for operation result."""

    result: float
    operation: OperationType
    operands: List[Operand] = Field(default_factory=list)

    def __str__(self) -> str:
        return f"Result: {self.result}, Operation: {self.operation}, Operands: {[str(op) for op in self.operands]}"


class ValidationError(BaseModel):
    """Model for validation errors."""

    field: str
    message: str

    def __str__(self) -> str:
        return f"{self.field}: {self.message}"
