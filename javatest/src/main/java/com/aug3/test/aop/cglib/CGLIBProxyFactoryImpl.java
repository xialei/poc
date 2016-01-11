package com.aug3.test.aop.cglib;

import net.sf.cglib.proxy.Enhancer;
import net.sf.cglib.proxy.MethodInterceptor;

import com.aug3.test.aop.AOPInterceptor;

public class CGLIBProxyFactoryImpl implements CGLIBProxyFactory {

	public <T> T createProxy(Class<T> clazz, AOPInterceptor interceptor) {
		MethodInterceptor methodInterceptor = new CGLIBMethodInterceptor(interceptor);

		Enhancer enhancer = new Enhancer();
		enhancer.setSuperclass(clazz);
		enhancer.setCallback(methodInterceptor);
		// configure CallbackFilter to map a method to a callback
		// enhancer.setCallbackFilter(CallbackFilter)
		return (T) enhancer.create();
	}
}