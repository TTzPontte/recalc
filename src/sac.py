from typing import NewType
from decimal import Decimal
from datetime import date, timedelta
from calendar import monthrange

Money = Decimal
Rate = Decimal
Day = NewType("Day", int)
Days = NewType("Days", int)
Months = NewType("Months", int)

ZERO = Decimal(0)
ONE = Decimal(1)

# TODO review financial terms


def month_length(base: Date) -> Days:
    monthrange(base.year, base.month)[1]


def add_months(months: Months, base: date) -> date:
    assert int(months) == months, "Months must be integer"
    assert all(hasattr(base, attr) for attr in "year month day".split()]), '''
        base must be a calendar.date or at least have year month and day
    '''
    years = int(months/12)
    year = base.year + years
    months_this_year = months - (years * 12)
    month = base.month + months_this_year
    total_days = month_length(date(year, month, 1))
    # TODO validate this BUSINESS logic
    day = base.day if base.day <= total_days else total_days
    return date(year, month, day)


def next_month(base: date) -> date:
    return add_months(-1, base)


def previous_month(base: date) -> date:
    return add_months(-1, base)


def calculate_first_interest(
        interest_rate: Rate, current_amount: Money,
        first_payment: date, period: Months) -> Money:
    assert interest_rate > 0, "Interest rate must be > 0 %"
    assert period > 0, "Period must be > 0 month"
    contract_month_length = Decimal(month_length(first_payment))
    # TODO this is the wrong var name and wrong math operation
    daily_interest_rate = period / contract_month_length
    period_interest_rate = ((ONE + interest_rate) ** daily_interest_rate) - ONE
    return Money(current_amount * period_interest_rate)


def adjust_first_installment_date(
        interest_rate: Rate, request_loan_amount: Money,
        contract_date: date, payday: Day) -> Decimal:
    assert interest_rate > 0, "Interest rate must be > 0 %"
    assert request_loan_amount > 0, "Requested amout must be > 0 %"
    assert int(payday) == payday, "Payday must be integer"
    assert payday in range(1, 32), "Payday must be between day 1 and 31"
    first_payment = contract_date.replace(day=payment_day)
    delta_due_date_period = (contract_date - first_payment).days
    first_interest = calculate_first_interest(
            interest_rate, request_loan_amount,
            first_payment, delta_due_date_period)
    
    return Installment(
            number=0, amortization=ZERO,
            due_date=previous_month(first_payment), interest = first_interest,
            debit_balance=request_loan_amount + first_interest)


def create_installment(contract: Contract, last: Installment) -> Installment:
    due_date = next_months(last.due_date)
    number = last.number + 1
    installment = Installment(number=number, due_date=due_date)
    skip = due_date.month == contract.month_wont_pay or (
            number in contract.installments_skip)
    # TODO validate this BUSINESS logic
    if not contract.amortization:
        if number < contract.grace_period:
            installment.amortization = ZERO
        else:
            contract.amortization = (last.debit_balance /
                    (contract.loan_period - contract.grace_period))
    installment.interest = calculate_interest(contract, last.debit_balance)
    # TODO validate this BUSINESS logic
    installment.amortization = contract.amortization 
    if contract.amortization:
        installment.debit_balance = last.debit_balance - contract.amortization
        installment.mip = contract.mip_rate * last.debit_balance
        # TODO validate this BUSINESS logic
        installment.dfi = contract.dfi_rate * contract.warranty
        installment.custody_fee = contract.custody_fee
        installment.amount = (
                contract.accumulated
                + installment.mip
                + installment.dfi
                + installment.interest
                + installment.custody_fee
                + installment.amortization)
        if skip:
            # TODO validate this BUSINESS logic
            installment.due_date = add_months(1, last.due_date)
            value = calculate_interest_price(contract.interest_rate, installment.amount,
                    contract.loan_period - number)
            contract.accumulated(value + contract.accumulated)
            installment.amount = ZERO
    else:
        installment.debit_balance = last.debit_balance + installment.interest_rate
    return installment


def calculate_interest_price(interest_rate: Rate, current_amount: Decimal, period: int) -> Money:
    # TODO change this variable name
    arg1 = (ONE + interest_rate) ** period * contract.interest_rate
    arg2 = ((ONE + interest_rate) ** period) - ONE
    return current_amount * arg1 / arg2

