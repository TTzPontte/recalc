package he.loan.calculator.model;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDate;

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
public class ContractInstallmentDto implements Serializable{

	private static final long serialVersionUID = 883996851514819362L;
	
	private int number;
	private LocalDate dueDate;
	
	@Builder.Default
	private BigDecimal amortization = BigDecimal.ZERO;
	
	@Builder.Default
	private BigDecimal interest = BigDecimal.ZERO;
	
	@Builder.Default
	private BigDecimal contractDebitBalance = BigDecimal.ZERO;
	
	@Builder.Default
	private BigDecimal mipInsurance = BigDecimal.ZERO;
	
	@Builder.Default
	private BigDecimal dfiInsurance = BigDecimal.ZERO;
	
	@Builder.Default
	private BigDecimal admnistrativeRate = BigDecimal.ZERO;
	
	@Builder.Default
	private BigDecimal amount = BigDecimal.ZERO;
	
}
