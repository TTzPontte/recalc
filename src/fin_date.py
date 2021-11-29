'''
Dates has no catersian logic
But finnancial math has some standards
'''

from typing import NewType
from datetime import date, timedelta
from calendar import monthrange


Days = NewType("Days", int)
Day = NewType("Day", int)
Months = NewType("Months", int)
Month = NewType("Month", int)
Date = date


def month_length(base: Date) -> Days:
    return monthrange(base.year, base.month)[1]


def add_months(months: Months, base: Date) -> Date:
    '''
    This is based on JAVA implementation of add month
    '''
    assert int(months) == months, "Months must be integer"
    assert all(hasattr(base, attr) for attr in "year month day".split()), '''
        base must be a calendar.date or at least have year month and day
    '''
    years = int((base.month + months) / 13)
    year = base.year + years
    months_this_year = months - (years * 12)
    month = base.month + months_this_year

    total_days = month_length(date(year, month, 1))
    # TODO validate this BUSINESS logic
    day = base.day if base.day <= total_days else total_days
    return date(year, month, day)


def next_month(base: Date) -> Date:
    return add_months(1, base)


def previous_month(base: Date) -> Date:
    return add_months(-1, base)
