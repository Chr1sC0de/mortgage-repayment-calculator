import datetime as dt


def is_end_of_month(date: dt.date) -> bool:
    return (date + dt.timedelta(days=1)).month != date.month


def is_end_of_year(date: dt.date) -> bool:
    return (date + dt.timedelta(days=1)).year != date.year
