package com.aug3.test.aop.guice;

import com.google.inject.Guice;
import com.google.inject.Injector;

public class BillingService {

	@TimeLog
	public void doBusiness() {
		System.out.println("DO BUSI");
	}
	
	public static void main(String args[]) {

		Injector injector = Guice.createInjector(new InterceptorModule());
		BillingService bs = new BillingService();
		injector.injectMembers(bs);
		bs.doBusiness();
	}

	

}
