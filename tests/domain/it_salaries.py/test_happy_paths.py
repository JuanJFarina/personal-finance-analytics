from personal_finance_analytics.domain.it_salaries import get_inflation_scalar


def test_get_inflation_scalar():
    result = get_inflation_scalar(1)
    assert isinstance(result, float)
    assert result > 1
