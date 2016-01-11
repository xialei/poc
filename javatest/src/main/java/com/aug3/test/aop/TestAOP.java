package com.aug3.test.aop;

import com.aug3.test.aop.annotation.TransactionInterceptor;
import com.aug3.test.aop.cglib.CGLIBProxyFactory;
import com.aug3.test.aop.cglib.CGLIBProxyFactoryImpl;
import com.aug3.test.aop.dyna.DynamicProxyFactory;
import com.aug3.test.aop.dyna.DynamicProxyFactoryImpl;

public class TestAOP {

	public static void main(String[] args) {
		AOPInterceptor interceptor = new TransactionInterceptor();

		DynamicProxyFactory proxyFactory = new DynamicProxyFactoryImpl();
		PersistenceService persistenceService = proxyFactory.createProxy(PersistenceService.class,
				new PersistenceServiceImpl(), interceptor);
		persistenceService.save(1, "Jason Zhicheng Li");
		String data = persistenceService.load(1);
		System.out.println(data);

		CGLIBProxyFactory cglib = new CGLIBProxyFactoryImpl();
		PersistenceService p = cglib.createProxy(PersistenceServiceImpl.class, interceptor);
		p.save(2, "hello cglib");
		data = p.load(2);
		System.out.println(data);

		BusinessWorker busi = new BusinessWorker();
		busi.doBusinessWork();
	}

}
