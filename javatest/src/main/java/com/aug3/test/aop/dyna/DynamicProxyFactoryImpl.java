package com.aug3.test.aop.dyna;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Proxy;

import com.aug3.test.aop.AOPInterceptor;

public class DynamicProxyFactoryImpl implements DynamicProxyFactory {

	@Override
	public <T> T createProxy(Class<T> clazz, T target, AOPInterceptor interceptor) {
		InvocationHandler handler = new DynamicProxyInvocationHandler(target, interceptor);
		return (T) Proxy.newProxyInstance(Thread.currentThread().getContextClassLoader(), new Class<?>[] { clazz },
				handler);

	}
}
