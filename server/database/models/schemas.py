from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class BaseSchema(BaseModel):
    """Базовые настройки."""

    model_config = ConfigDict(from_attributes=True)


class EmployeeCreate(BaseSchema):
    name: str
    email: EmailStr


class EmployeeResponse(EmployeeCreate, BaseSchema):
    id: int


class EmployeeListResponse(BaseSchema):
    items: list[EmployeeResponse]
    total: int
    page: Optional[int] = None
    limit: Optional[int] = None


class Error(BaseModel):
    error: str
