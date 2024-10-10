from abc import ABC, abstractmethod
from typing import Any, Union

from app.core.base.operation.types import OperationResult, OperationType


class Operation(ABC):
    """Base class for all operations."""

    def __init__(self, operation_type: OperationType):
        self.operation_type = operation_type

    @abstractmethod
    def execute(
        self, a: Union[int, float], b: Union[int, float], **kwargs: Any
    ) -> OperationResult:
        """Execute the operation and return the result.

        Args:
            a (Union[int, float]): First operand.
            b (Union[int, float]): Second operand.
            kwargs (Any): Additional arguments if any.

        Returns:
            OperationResult: The result of the operation.
        """
        pass
