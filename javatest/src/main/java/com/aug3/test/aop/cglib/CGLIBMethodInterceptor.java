package com.aug3.test.aop.cglib;

import java.lang.reflect.Method;

import net.sf.cglib.proxy.MethodInterceptor;
import net.sf.cglib.proxy.MethodProxy;

import com.aug3.test.aop.AOPInterceptor;

public class CGLIBMethodInterceptor implements MethodInterceptor {

	private AOPInterceptor interceptor;

	public CGLIBMethodInterceptor(AOPInterceptor interceptor) {
		this.interceptor = interceptor;
	}

	@Override
	public Object intercept(Object object, Method method, Object[] args, MethodProxy methodProxy) throws Throwable {
		try {
			interceptor.before(method, args);
			Object returnValue = methodProxy.invokeSuper(object, args);
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
