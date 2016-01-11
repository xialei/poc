package com.aug3.test.my;

public class Credit {

	private int remainingTerm;

	private int remainingAmount;

	private int annualRate;

	public double getDefaultProbability(int remDays) {
		if (remDays < 30)
			return 0.9;
		else if (remDays < 60)
			return 0.7;
		else if (remDays < 90)
			return 0.5;
		else
			return 0.2;
	}

	public int getRemainingTerm() {
		return remainingTerm;
	}

	public void setRemainingTerm(int remainingTerm) {
		this.remainingTerm = remainingTerm;
	}

	public int getRemainingAmount() {
		return remainingAmount;
	}

	public void setRemainingAmount(int remainingAmount) {
		this.remainingAmount = remainingAmount;
	}

	public int getAnnualRate() {
		return annualRate;
	}

	public void setAnnualRate(int annualRate) {
		this.annualRate = annualRate;
	}

}
