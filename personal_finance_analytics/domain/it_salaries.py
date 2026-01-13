import pandas as pd


from pathlib import Path

from pydantic import BaseModel

from personal_finance_analytics.utils import JuniorToSeniorDeltaException

from .entities import SenioritySalary

from .months import get_months_since

from .salaries import get_current_month_salary, get_salaries_data


CWD_PATH = Path(__file__).parent.parent.resolve()


def get_inflation_scalar(months: int) -> float:
    salaries_csv = get_salaries_data()
    scalar = 1
    for m in range(months, 0, -1):
        last_month_inflation = salaries_csv["inflacion_del_mes_anterior"].iloc[-m]
        scalar *= 1 + (last_month_inflation * 0.01)
    return scalar


def get_sysarmy_data() -> pd.DataFrame:
    sysarmy_data = pd.read_csv(
        CWD_PATH / "data" / "2025_2_sysarmy.csv",
        usecols=[
            "dedicacion",
            "ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos",
            "seniority",
        ],
    )
    sysarmy_data["ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"] = (
        sysarmy_data["ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"]
        * get_inflation_scalar(get_months_since(7))
    )
    return sysarmy_data


def prepare_sysarmy_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sysarmy = get_sysarmy_data()
    sysarmy_fulltime = sysarmy[sysarmy["dedicacion"] == "Full-Time"]

    sysarmy_fulltime = sysarmy[
        (sysarmy["dedicacion"] == "Full-Time")
        & (
            sysarmy[
                "ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"
            ].notnull()
        )
    ]

    sysarmy_fulltime = sysarmy_fulltime.sort_values(
        by="ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"
    ).reset_index(drop=True)

    juniors = sysarmy_fulltime[sysarmy_fulltime["seniority"] == "Junior"]
    semiseniors = sysarmy_fulltime[sysarmy_fulltime["seniority"] == "Semi-Senior"]
    seniors = sysarmy_fulltime[sysarmy_fulltime["seniority"] == "Senior"]

    juniors_90 = juniors[
        "ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"
    ].quantile(0.95)
    juniors = juniors[
        juniors["ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"]
        <= juniors_90
    ]

    semiseniors_90 = semiseniors[
        "ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"
    ].quantile(0.95)
    semiseniors_05 = semiseniors[
        "ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"
    ].quantile(0.05)
    semiseniors = semiseniors[
        semiseniors["ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"]
        <= semiseniors_90
    ]
    semiseniors = semiseniors[
        semiseniors["ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"]
        >= semiseniors_05
    ]

    seniors_90 = seniors[
        "ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"
    ].quantile(0.95)
    seniors_05 = seniors[
        "ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"
    ].quantile(0.05)
    seniors = seniors[
        seniors["ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"]
        <= seniors_90
    ]
    seniors = seniors[
        seniors["ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"]
        >= seniors_05
    ]
    return juniors, semiseniors, seniors


def get_current_it_salary() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "dedicacion": "Full-Time",
            "ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos": get_current_month_salary(),
            "seniority": "Sueldo Actual",
        },
        index=[0],
    )


def get_it_salaries_sorted() -> pd.DataFrame:
    juniors, semiseniors, seniors = prepare_sysarmy_data()
    current_salary = get_current_it_salary()
    sysarmy_ordenado = (
        pd.concat([juniors, semiseniors, seniors, current_salary])
        .sort_values(by="ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos")
        .reset_index(drop=True)
    )
    return sysarmy_ordenado


def get_it_salary_percentile() -> float:
    it_salaries_sorted = get_it_salaries_sorted()
    return (
        it_salaries_sorted.index[it_salaries_sorted["seniority"] == "Sueldo Actual"][0]
        * 100
    ) / len(it_salaries_sorted)


class RawSenioritySalary(BaseModel):
    label: str
    salary_float: float


def get_it_salary_rank_per_seniority() -> tuple[
    list[SenioritySalary], list[RawSenioritySalary]
]:
    juniors, semiseniors, seniors = prepare_sysarmy_data()
    current_it_salary = get_current_it_salary()
    summary = [
        current_it_salary["ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"][
            0
        ],
        juniors["ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"].mean(),
        juniors["ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"].median(),
        semiseniors["ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"].mean(),
        semiseniors[
            "ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"
        ].median(),
        seniors["ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"].mean(),
        seniors["ultimo_salario_mensual_o_retiro_neto_en_pesos_argentinos"].median(),
    ]

    labels = [
        "Personal Salary",
        "Juniors Mean",
        "Juniors Median",
        "Semi-Seniors Mean",
        "Semi-Seniors Median",
        "Seniors Mean",
        "Seniors Median",
    ]

    combined = list(zip(summary, labels))
    combined.sort(key=lambda x: x[0])
    return (
        [
            SenioritySalary(
                label=label,
                salary=f"$ {salary:,.0f}",
            )
            for salary, label in combined
        ],
        [
            RawSenioritySalary(label=label, salary_float=salary)
            for salary, label in combined
        ],
    )


def get_junior_to_senior_delta() -> str:
    salaries = get_it_salary_rank_per_seniority()[1]
    for seniority in salaries:
        if seniority.label == "Juniors Mean":
            junior_mean_salary = seniority
        if seniority.label == "Seniors Mean":
            senior_mean_salary = seniority
    if not junior_mean_salary or not senior_mean_salary:  # type: ignore
        raise JuniorToSeniorDeltaException(
            "Could not find junior or senior mean salary."
        )
    return f"{((senior_mean_salary.salary_float * 100) / junior_mean_salary.salary_float) - 100:.2f} % from Junior ($ {junior_mean_salary.salary_float:,.0f}) to Senior ($ {senior_mean_salary.salary_float:,.0f})"
