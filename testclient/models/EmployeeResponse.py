from typing import *

from pydantic import BaseModel, Field


class EmployeeResponse(BaseModel):
    """
    EmployeeResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    name: str = Field(validation_alias="name")

    email: str = Field(validation_alias="email")

    rate_per_hour: int = Field(validation_alias="rate_per_hour")

    id: int = Field(validation_alias="id")
