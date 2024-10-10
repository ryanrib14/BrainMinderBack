from typing import Union, Any
from app.core.base.operation.base import Operation
from app.core.base.operation.types import Operand, OperationResult, OperationType


class Divide(Operation):
    """Division operation."""

    def __init__(self) -> None:
        super().__init__(OperationType.DIVISION)

    def execute(
        self, a: Union[int, float], b: Union[int, float], **kwargs: Any
    ) -> OperationResult:
        result = a / b
        return OperationResult(
            result=result,
            operation=self.operation_type,
            operands=[Operand(value=a), Operand(value=b)],
        )

