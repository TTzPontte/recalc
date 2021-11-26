package he.loan.calculator.response;

import java.io.Serializable;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class DefaultResponseDto implements Serializable {

	private static final long serialVersionUID = 261163260937882990L;

    private Integer returnCode;

    private String returnMessage;

    private Object payload;
}