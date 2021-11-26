package he.loan.calculator.service;

import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

import he.loan.calculator.model.ContractDto;
import he.loan.calculator.model.ContractInstallmentDto;
import he.loan.calculator.request.ContractRequest;

@Service
public class LoanCalculatorSacService {

	public static final BigDecimal ONE_HUNDRED = new BigDecimal(100);
	private static ModelMapper mp = new ModelMapper();

	public ContractDto calculate(ContractRequest request) {

		ContractDto heContract = new ContractDto();
		mp.map(request, heContract);

		adjustFirstInstallmentDate(heContract);
		
		for (int i = 2; i <= heContract.getLoanPeriod() + 1; i++) {
			heContract.getInstallments().put(i, createInstallment(heContract, heContract.getInstallments().get(i - 1)));
		}
		return heContract;
	}

	private static void adjustFirstInstallmentDate(final ContractDto heContract) {

		LocalDate firstPayment = LocalDate.of(heContract.getContractDate().getYear(),
				heContract.getContractDate().getMonth().getValue() + 0, heContract.getPaymentDay());

		Long deltaDueDatePeriod = ChronoUnit.DAYS.between(heContract.getContractDate(), firstPayment);

		// calcular juros diario para fechar o mes
		BigDecimal firstInterest = calculateFirstInterest(heContract, heContract.getRequestLoanAmount(), firstPayment,
				deltaDueDatePeriod.intValue());

		ContractInstallmentDto adjustInstallment = ContractInstallmentDto.builder().number(0)
				.amortization(BigDecimal.ZERO).dueDate(firstPayment.minusMonths(1))
				.contractDebitBalance(heContract.getRequestLoanAmount().add(firstInterest)).interest(firstInterest)
				.build();

		heContract.getInstallments().put(1, adjustInstallment);

	}

	private static ContractInstallmentDto createInstallment(final ContractDto heContract,
			final ContractInstallmentDto lastInstallment) {

		ContractInstallmentDto installment = ContractInstallmentDto.builder().number(lastInstallment.getNumber() + 1)
				.dueDate(lastInstallment.getDueDate().plusMonths(1)).build();

		// VALIDAR SE PARCELA SERA PULADA
		Boolean skip = heContract.getInstallmentsSkip().contains(installment.getNumber()) || heContract.getMonthWontPay() == installment.getDueDate().getMonth().getValue();

		// Contrato sem amortizacao
		if (heContract.getAmortization().compareTo(BigDecimal.ZERO) == 0) {

			if (installment.getNumber() <= heContract.getGracePeriod()) {
				installment.setAmortization(BigDecimal.ZERO);

			} else {
				BigDecimal amortization = lastInstallment.getContractDebitBalance().divide(
						new BigDecimal(heContract.getLoanPeriod() - heContract.getGracePeriod()),
						MathContext.DECIMAL32);

				heContract.setAmortization(amortization);
			}
		}

		installment.setInterest(calculateInterest(heContract, lastInstallment.getContractDebitBalance()));
		installment.setAmortization(heContract.getAmortization());

		if (heContract.getAmortization().compareTo(BigDecimal.ZERO) > 0) {
			installment.setContractDebitBalance(
					lastInstallment.getContractDebitBalance().subtract(heContract.getAmortization()));

			installment.setMipInsurance(
					heContract.getMipInsurancePercentage().multiply(lastInstallment.getContractDebitBalance()));
			installment.setDfiInsurance(heContract.getDfiInsurancePercentage().multiply(heContract.getWarranty()));
			installment.setAdmnistrativeRate(heContract.getAdmnistrativeRateFixed());

			installment.setAmount(
					installment.getAmortization().add(heContract.getAccumulated()).add(installment.getInterest())
							.add(installment.getMipInsurance()).add(installment.getDfiInsurance())
							.add(installment.getAdmnistrativeRate()).setScale(2, RoundingMode.HALF_UP));

			if (skip) {
				// PULOU PARCELA
				installment.setDueDate(lastInstallment.getDueDate().plusMonths(1));
				BigDecimal value = calculateInterestPrice(heContract, installment.getAmount(),
						heContract.getLoanPeriod() - (installment.getNumber()));
				heContract.setAccumulated(value.add(heContract.getAccumulated()).setScale(2, RoundingMode.HALF_UP));

				// zerar parcela
				installment.setAmount(BigDecimal.ZERO);

			}

		} else {
			installment.setContractDebitBalance(lastInstallment.getContractDebitBalance().add(installment.getInterest()));
		}

		return installment;
	}

	private static BigDecimal calculateFirstInterest(final ContractDto heContract, final BigDecimal currentAmount,
			final LocalDate firstPayment, final int period) {

		BigDecimal dailyInterestRate = BigDecimal.valueOf(period)
				.divide(new BigDecimal(heContract.getContractDate().lengthOfMonth()), MathContext.DECIMAL32);
		
		BigDecimal periodInterestRate = BigDecimal.valueOf(Math.pow(BigDecimal.ONE.add(heContract.getInterestRate()).doubleValue(), dailyInterestRate.doubleValue()))
				.subtract(BigDecimal.ONE, MathContext.DECIMAL32);

		return currentAmount.multiply(periodInterestRate, MathContext.DECIMAL32);

	}

	private static BigDecimal calculateInterestPrice(final ContractDto heContract, final BigDecimal currentAmount,
			final int period) {

		BigDecimal arg1 = BigDecimal.ONE.add(heContract.getInterestRate()).pow(period).multiply(heContract.getInterestRate());
		BigDecimal arg2 = BigDecimal.ONE.add(heContract.getInterestRate()).pow(period).subtract(BigDecimal.ONE);

		return currentAmount.multiply(arg1.divide(arg2, MathContext.DECIMAL32));

	}

	private static BigDecimal calculateInterest(final ContractDto heContract, final BigDecimal currentAmount) {
		return currentAmount.multiply(heContract.getInterestRate(), MathContext.DECIMAL32);
	}

}
