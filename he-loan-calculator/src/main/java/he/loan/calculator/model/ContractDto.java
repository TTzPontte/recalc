package he.loan.calculator.model;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

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
public class ContractDto implements Serializable {

	private static final long serialVersionUID = -974723142956178320L;
	
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
	private BigDecimal accumulated = BigDecimal.ZERO;
	@Builder.Default
	private List<Integer> installmentsSkip = new ArrayList<>();
	private int monthWontPay;
	
	@Builder.Default
	private Map<Integer, ContractInstallmentDto> installments = new HashMap<>();
	
}
