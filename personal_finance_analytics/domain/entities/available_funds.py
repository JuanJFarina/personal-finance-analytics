from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


class CategoryFunds(BaseModel):
    category: str
    max_allocation: Annotated[str, Field(min_length=5)]
    available_funds: Annotated[str, Field(min_length=5)]


class AvailableFunds(BaseModel):
    net_salary: Annotated[str, Field(min_length=7)]
    category_funds: list[CategoryFunds]
    balance: Annotated[str, Field(min_length=3)]
    estimated_month_balance: Annotated[str, Field(min_length=3)]

    model_config = ConfigDict(arbitrary_types_allowed=True)
