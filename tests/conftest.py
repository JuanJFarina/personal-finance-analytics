import pytest
import pandas as pd


@pytest.fixture
def current_month_expenses_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "category": ["Food", "Transportation", "Entertainment"],
            "amount": [500.0, 200.0, 150.0],
        }
    )


@pytest.fixture
def current_month_salary() -> float:
    return 2_000_000.00
