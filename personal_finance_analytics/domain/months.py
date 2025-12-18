from datetime import datetime

MONTHS = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]


def get_months_until_now():
    current_month = datetime.now().month
    return MONTHS[:current_month]


def get_next_month() -> str:
    current_month = datetime.now().month
    if current_month == 12:
        return MONTHS[0]
    return MONTHS[current_month - 1]
