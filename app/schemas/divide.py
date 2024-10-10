from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID


class DivideOperationObject(BaseModel):
    id: UUID
    a: float
    b: float
    result: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class DivideRequest(BaseModel):
    a: float = Field(...)
    b: float = Field(...)

    @field_validator("b")
    def b_must_not_be_zero(cls, v: float) -> float:
        if v == 0:
            raise ValueError("The divisor (b) must not be zero.")
        return v


class DivideResponse(BaseModel):
    result: float
