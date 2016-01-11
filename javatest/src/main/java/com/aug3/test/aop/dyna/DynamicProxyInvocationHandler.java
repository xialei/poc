package com.aug3.test.aop.dyna;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;

import com.aug3.test.aop.AOPInterceptor;

public class DynamicProxyInvocationHandler implements InvocationHandler {

	private Object target;
	private AOPInterceptor interceptor;

	public DynamicProxyInvocationHandler(Object target, AOPInterceptor interceptor) {
		this.target = target;
		this.interceptor = interceptor;
	}

	@Override
	public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
		try {
			interceptor.before(method, args);
			Object returnValue = method.invoke(target, args);
			interceptor.after(method, args);
			return returnValue;
		} catch (Throwable t) {
			interceptor.afterThrowing(method, args, t);
			throw t;
		} finally {
			interceptor.afterFinally(method, args);
		}
	}
}
