package com.aug3.test.aop;

import java.lang.reflect.Method;

public interface AOPInterceptor {

	void before(Method method, Object[] args);

	void after(Method method, Object[] args);

	void afterThrowing(Method method, Object[] args, Throwable throwable);

	void afterFinally(Method method, Object[] args);

}
