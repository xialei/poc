package com.aug3.test.aop.dyna;

import com.aug3.test.aop.AOPInterceptor;

public interface DynamicProxyFactory {

	<T> T createProxy(Class<T> clazz, T target, AOPInterceptor interceptor);

}
