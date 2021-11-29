{
  config.files.gitignore.pattern."events" = true;
  config.files.json."events/sac.json".body = builtins.toJSON {
    loanCalculationType = "SAC";
    contractDate = "2021-11-16";
    paymentDay = 16;
    requestLoanAmount = 100000;
    loanPeriod = 10;
    warranty = 500000;
    interestRate = 0.0079;
    gracePeriod = 0;
    amortization = 10000.0;
    mipInsurancePercentage = 0.00021;
    dfiInsurancePercentage = 0.00007;
    admnistrativeRateFixed = 25;
    installmentsSkip = [5 8 104];
    monthWontPay = 0;
  };
}
