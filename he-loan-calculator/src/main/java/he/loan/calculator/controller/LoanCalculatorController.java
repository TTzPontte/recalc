package he.loan.calculator.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import he.loan.calculator.request.ContractRequest;
import he.loan.calculator.response.DefaultResponseDto;
import he.loan.calculator.service.LoanCalculatorSacService;

@RestController
@RequestMapping
public class LoanCalculatorController {
	
	@Autowired
	LoanCalculatorSacService loanCalculatorSacService;
	
	
	@PostMapping("/sac")
	public Object calculateSac(@RequestBody ContractRequest contract) {
		return new DefaultResponseDto(HttpStatus.OK.value(), null,
				loanCalculatorSacService.calculate(contract));
	}
	
	@GetMapping("/price")
	public Object calculatePrice() {
		return null;
		
	}

}
