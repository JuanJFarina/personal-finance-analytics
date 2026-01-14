from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


class SenioritySalary(BaseModel):
    label: Annotated[str, Field(min_length=5)]
    salary: Annotated[str, Field(min_length=7)]


class SalaryAnalytics(BaseModel):
    net_salary: Annotated[str, Field(min_length=7)]
    adjusted_salary: Annotated[str, Field(min_length=7)]
    salary_variance_in_usd: Annotated[str, Field(min_length=10)]
    it_salary_percentile: Annotated[str, Field(min_length=2)]
    rank_per_seniority: list[SenioritySalary]
    junior_to_senior_delta: Annotated[str, Field(min_length=2)]
    personal_delta: Annotated[str, Field(min_length=2)]
    it_delta_adjusted_salary: Annotated[str, Field(min_length=7)]

    model_config = ConfigDict(arbitrary_types_allowed=True)
