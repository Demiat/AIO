from typing import *

from pydantic import BaseModel, Field

from .EmployeeResponse import EmployeeResponse


class EmployeeListResponse(BaseModel):
    """
    EmployeeListResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    items: List[EmployeeResponse] = Field(validation_alias="items")

    total: int = Field(validation_alias="total")

    page: Optional[int] = Field(validation_alias="page", default=None)

    limit: Optional[int] = Field(validation_alias="limit", default=None)
