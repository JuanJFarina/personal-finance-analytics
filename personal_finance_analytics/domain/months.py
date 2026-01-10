from datetime import datetime
import logging

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


def get_months_since(month: int) -> int:
    current_month = datetime.now().month
    if month > current_month:
        return 12 - month + current_month
    return current_month - month


def get_current_month() -> str:
    current_month = datetime.now().month
    logging.info(f"Current month index: {current_month}")
    return MONTHS[current_month - 1]


def get_next_month() -> str:
    current_month = datetime.now().month
    logging.info(f"Current month index: {current_month}")
    if current_month == 12:
        return MONTHS[0]
    return MONTHS[current_month]
