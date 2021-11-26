package he.loan.calculator.request;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

import he.loan.calculator.enums.LoanCalculationType;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ContractRequest {
	
private LoanCalculationType loanCalculationType;
	
	private LocalDate contractDate;
	
	private int paymentDay;
	
	@Builder.Default
	private BigDecimal requestLoanAmount = BigDecimal.ZERO;;
	
	private int loanPeriod;
	
	private BigDecimal interestRate;
	
	@Builder.Default
	private int gracePeriod = 0;
	
	@Builder.Default
	private BigDecimal amortization = BigDecimal.ZERO;
	
	//
	private BigDecimal mipInsurancePercentage;
	private BigDecimal dfiInsurancePercentage;
	private BigDecimal admnistrativeRateFixed;
	@Builder.Default
	private BigDecimal warranty = BigDecimal.ZERO;
	@Builder.Default
	private List<Integer> installmentsSkip = new ArrayList<>();
	private int monthWontPay;

}
