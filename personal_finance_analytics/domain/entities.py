from pydantic import BaseModel, ConfigDict


class CategoryFunds(BaseModel):
    category: str
    max_allocation: str
    available_funds: str


class AvailableFunds(BaseModel):
    net_salary: str
    category_funds: list[CategoryFunds]
    balance: str
    estimated_month_balance: str

    model_config = ConfigDict(arbitrary_types_allowed=True)
