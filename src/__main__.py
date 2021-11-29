from typing import Dict, Any
from json import loads, load
from datetime import date
from dataclasses import asdict, is_dataclass
from .http_wrapper import http
from .sac import calculate, Contract
from .fin_types import Money, Rate, AmortizationMethod
from .fin_date import (
    Date, Day, Days, Months, Month,
    month_length, add_months, next_month, previous_month)


def contract(payload: Dict[str, Any]) -> Contract:
    custody_fee = payload.get("admnistrativeRateFixed", None)
    assert type(custody_fee) in (int, float) and custody_fee >= 0, f'''
        admnistrativeRateFixed deve ser valor $ da taxa admistrativa >= 0
        recebido {custody_fee}
    '''

    amortization = payload.get("amortization", None)
    assert type(amortization) in (int, float) and amortization >= 0, f'''
        amortization deve ser o valor $ da amortização >= 0
        recebido {amortization}
    '''

    contract_date = None
    try:
        contract_date_str = payload.get("contractDate", None)
        contract_date = date.fromisoformat(contract_date_str)
    except:
        raise
        assert contract_date is not None, f'''
           contractDate deve ser uma data em formato ISO 8601
           recebido {contract_date}
        '''

    dfi = payload.get("dfiInsurancePercentage", None)
    assert type(dfi) in (int, float) and dfi >= 0, f'''
        dfiInsurancePercentage deve ser a taxa % do segudo dfi >= 0
        recebido {dfi}
    '''

    mip = payload.get("mipInsurancePercentage", None)
    assert type(mip) in (int, float) and mip >= 0, f'''
        mpiInsurancePercentage deve ser a taxa % do seguro mip >= 0
        recebido {mip}
    '''
    grace_period = payload.get("gracePeriod", None)

    assert type(grace_period) == int and grace_period >= 0, f'''
        gracePeriod deve ser a carência em meses (inteiro)
        recebido {grace_period}
    '''

    installments_skip = payload.get("installmentsSkip", None)
    assert installments_skip is not None, f'''
        installmentsSkip deve ser lista de meses sem pagar ou uma lista vazia
        recebido {installments_skip}
    '''
    assert all(type(i) == int for i in installments_skip), f'''
        installmentsSkip deve ser lista de meses sem pagar e devem ser numeros inteiro
        recebido {installments_skip}
    '''
    assert all(i > 0 for i in installments_skip), f'''
        installmentsSkip deve ser lista de meses sem pagar, de 1 e o fim do contrato
        recebido {installments_skip}
    '''

    interest_rate = payload.get("interestRate", None)
    assert type(interest_rate) in (int, float) and interest_rate > 0, f'''
        interestRate deve ser a taxa % de juros, numero > 0
        recebido {interest_rate}
    '''

    amortization_method = payload.get("loanCalculationType", None)
    assert amortization_method == "SAC", f'''
        loanCalculationType deve ser como será calculada amortizatização ('sac')
        recebido {amortization_method}
    '''

    loan_period = payload.get("loanPeriod", None)
    assert type(loan_period) == int and loan_period > 0, f'''
        loanPeriod deve ser o total de meses do contrato, inteiro > 0
        recebido {loan_period}
    '''

    month_wont_pay = payload.get("monthWontPay", None)
    assert type(month_wont_pay) == int and month_wont_pay >= 0 and month_wont_pay <= 12, f'''
        monthWontPay deve ser 0 ou o mẽs sem cobrar a parcela >= 1 e <= 12
        recebido {month_wont_pay}
    '''

    payday = payload.get("paymentDay", None)
    assert type(payday) == int and payday >= 0 and payday <=31, f'''
        paymentDay deve ser o dia do vencimento das parcelas >= 1 e <= 31
        recebido {payday}
    '''

    request_loan_amount = payload.get("requestLoanAmount", None)
    assert type(request_loan_amount) in (int, float) and request_loan_amount >= 0, f'''
        requestLoanAmount deve ser o valor $ do emprestimo > 0
        recebido {request_loan_amount}
    '''

    warranty = payload.get("warranty", None)
    assert type(warranty) in (int, float) and warranty > 0, f'''
        warranty deve ser o valor $ do bem dado como garantia > 0
        recebido {warranty}
    '''

    return Contract(
        custody_fee=Money(custody_fee),
        amortization=Money(amortization),
        contract_date=contract_date,
        dfi=Rate(dfi),
        mip=Rate(mip),
        grace_period=Months(grace_period),
        installments_skip=installments_skip,
        interest_rate=Rate(interest_rate),
        amortization_method=AmortizationMethod[amortization_method],
        loan_period=Months(loan_period),
        month_wont_pay=Month(month_wont_pay),
        payday=Day(payday),
        request_loan_amount=Money(request_loan_amount),
        warranty=Money(warranty),
        installments=[])


@http
def handle(event, context):
    evt_body = event.get("body", None)
    assert type(evt_body) == str, f'''
        Esperado receber o body em formato JSON
        recebido {type(evt_body)}
    '''

    payload = None
    try:
        payload = loads(evt_body)
    except:
        pass
    assert type(payload) == dict, f'''
        Esperado receber body em formato JSON contendo um objeto
        recebido {type(payload)}
        {payload}
    '''

    return calculate(
        contract(payload)
    )


if __name__ == "__main__":
    from os import path
    from .encoder import dumps
    event_file = path.join(path.dirname(__file__), '../events/sac.json')
    event = {}
    context = {}
    with open(event_file) as sac_event:
        event = load(sac_event)
    response = handle(event, context)
    print(dumps(response))
