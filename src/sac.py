from typing import NewType, Dict, List, Any
from decimal import Decimal
from .fin_consts import ZERO, ONE
from .fin_types import Money, Rate, AmortizationMethod
from .fin_date import (
    Date, Day, Days, Months, Month,
    month_length, add_months, next_month, previous_month)

from dataclasses import dataclass, field



@dataclass
class Installment:
    number: int
    due_date: Date
    amortization: Money = field(default=ZERO)
    interest: Money = field(default=ZERO)
    debit_balance: Money = field(default=ZERO)


@dataclass
class Contract:
    custody_fee: Money
    amortization: Money
    contract_date: Date
    dfi: Rate
    mip: Rate
    grace_period: Months
    installments_skip: List[Months]
    interest_rate: Rate
    amortization_method: AmortizationMethod
    loan_period: Months
    month_wont_pay: Month
    payday: Day
    request_loan_amount: Money
    warranty: Money
    installments: List[Installment]
    accumulated: Money = field(default=ZERO)


def calculate_first_interest(
        interest_rate: Rate, current_amount: Money,
        first_payment: Date, period: Days) -> Money:
    assert interest_rate > 0, "Interest rate must be > 0 %"
    # TODO 0 period is same day or next month?
    assert period >= 0, "Period must be > 0 month"
    contract_month_length = month_length(first_payment)
    # TODO this is the wrong var name and wrong math operation
    daily_interest_rate = Decimal(period / contract_month_length)
    period_interest_rate = ((ONE + interest_rate) ** daily_interest_rate) - ONE
    return Money(current_amount * period_interest_rate)


def first_installment(
        interest_rate: Rate, request_loan_amount: Money,
        contract_date: Date, payday: Day) -> Installment:
    assert interest_rate > 0, "Interest rate must be > 0 %"
    assert request_loan_amount > 0, "Requested amout must be > 0 %"
    assert int(payday) == payday, "Payday must be integer"
    assert payday in range(1, 32), "Payday must be between day 1 and 31"
    first_payment = contract_date.replace(day=payday)
    delta_due_date_period = (contract_date - first_payment).days
    first_interest = calculate_first_interest(
            interest_rate, request_loan_amount,
            first_payment, delta_due_date_period)
    
    return Installment(
            number=0, amortization=ZERO,
            due_date=previous_month(first_payment), interest = first_interest,
            debit_balance=request_loan_amount + first_interest)


def calculate_interest_price(interest_rate: Rate, current_amount: Money, period: Months) -> Money:
    assert interest_rate > 0, "Interest rate should be > 0"
    assert current_amount > 0, "Current amount should be > 0"
    assert period > 0, "Period should be > 0"
    # TODO change this variable name
    arg1 = (ONE + interest_rate) ** period * interest_rate
    arg2 = ((ONE + interest_rate) ** period) - ONE
    return current_amount * arg1 / arg2


def calculate_interest(interest_rate: Rate, current_amount: Money) -> Money:
    assert interest_rate > 0, "Interest rate should be > 0"
    assert current_amount > 0, "Current amount should be > 0"
    return current_amount * interest_rate


def create_installment(contract: Contract, last: Installment) -> Installment:
    due_date = next_month(last.due_date)
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
    installment.interest = calculate_interest(contract.interest_rate, last.debit_balance)
    # TODO validate this BUSINESS logic
    installment.amortization = contract.amortization 
    if contract.amortization:
        installment.debit_balance = last.debit_balance - contract.amortization
        # TODO validate this BUSINESS logic
        installment.mip = contract.mip * last.debit_balance
        # TODO validate this BUSINESS logic
        installment.dfi = contract.dfi * contract.warranty
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
            installment.due_date = next_month(last.due_date)
            value = calculate_interest_price(contract.interest_rate, installment.amount,
                    contract.loan_period - number)
            contract.accumulated = value + contract.accumulated
            installment.amount = ZERO
    else:
        installment.debit_balance = last.debit_balance + installment.interest_rate
    return installment


def calculate(contract: Contract) -> Contract:
    last = first_installment(
        contract.interest_rate,
        contract.request_loan_amount,
        contract.contract_date,
        contract.payday)
    contract.installments = [ last ]
    for i in range(2, contract.loan_period + 1):
        last = create_installment(contract, last)
        contract.installments.append(last)
    return contract


